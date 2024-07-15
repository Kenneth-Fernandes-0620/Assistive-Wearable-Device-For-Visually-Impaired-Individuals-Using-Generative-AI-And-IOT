import logging
import signal
import threading
import time
from queue import Queue
from typing import List
import spacy

from audio_processing import (
    capture_speech,
    load_speech_capture,
)
from util import load_logger
from image_processing import get_image_from_webcam, load_image_capture
from networking import upload_image

messageQueue: Queue = None
resultQueue: Queue = None
logQueue: Queue = None
isRunning: bool = False
isWaiting: bool = True

logger: logging.Logger = None

commands: List[str] = [
    "describe environment",
    "SOS",
    "help",
]


# TODO: Add Documentation
def startup_worker():  # Function to load the model and audio and initialize the message queue and isRunning flag
    global messageQueue, resultQueue, isRunning, isWaiting, logQueue

    messageQueue = Queue()
    resultQueue = Queue()
    logQueue = Queue()

    isRunning = True
    isWaiting = False

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

def match_command(speech: str) -> Optional[str]:
    """
    This function takes a string input and determines if it matches any of the predefined commands using NLP.
    If a match is found, it returns the command; otherwise, it returns None.
    """
    doc = nlp(speech.lower().strip())
    for command in commands:
        command_doc = nlp(command)
        similarity = doc.similarity(command_doc)
        if similarity > 0.75:  # Adjust the similarity threshold as needed
            return command
    return None

def image_processing_worker():
    global isRunning, isWaiting, logQueue
    load_image_capture()
    try:
        while isRunning:
            if not messageQueue.empty():
                message: str = messageQueue.get()
                if message == commands[0]:
                    success, image = get_image_from_webcam()
                    if not success:
                        logQueue.put(
                            ("Unable to capture image from camera", logging.ERROR)
                        )
                        raise Exception("Unable to capture image from camera")
                    else:
                        logQueue.put(("Captured image from camera", logging.INFO))
                    try:
                        response = upload_image(image)
                        resultQueue.put(response.json()["caption"])
                    except Exception as e:
                        logQueue.put(
                            (f"Error in uploading image, {e.args[0]}", logging.ERROR)
                        )
                elif message == commands[1] or message == commands[2]:
                    logQueue.put(("Sending SOS signal...", logging.INFO))
                    raise Exception("Unimplemented command: SOS or help")
                isWaiting = False
            else:
                time.sleep(0.5)
    except Exception as e:
        print(e.args[0])
        logQueue.put((f"Error in image processing worker: {e.args[0]}", logging.ERROR))
        isRunning = False


def logging_worker():
    global isRunning, logger, logQueue
    logger = load_logger(__name__)

    logger.info("Logging worker started.")

    while isRunning:
        if not logQueue.empty():
            log_message: str = logQueue.get()
            logger.info(log_message[0])
        else:
            time.sleep(0.5)
    if not logQueue.empty():
        log_message: str = logQueue.get()
        logger.info(log_message[0])
    logger.info("Logging worker finished.")


# TODO: Add Documentation
def speech_processing_worker():
    global isRunning, isWaiting, logQueue
    load_speech_capture()
    logQueue.put(("Speech processing worker started.", logging.INFO))
    try:
        while isRunning:
            while not isWaiting:
                result: str = capture_speech()
                if result != None and result.lower().strip() in commands:
                    messageQueue.put(result.lower().strip())
                    logQueue.put(("Message received from user.", logging.INFO))
                    isWaiting = True
            if isWaiting:
                time.sleep(0.5)
    except Exception as e:
        logQueue.put((f"Error in audio processing worker: {e}", logging.ERROR))
        isRunning = False
    logQueue.put(("Speech processing worker finished.", logging.INFO))


def handle_terminate(_sig, _frame):
    global isRunning, isWaiting
    logQueue.put(("Kill signal received, exiting...", logging.CRITICAL))
    isWaiting = True
    isRunning = False


signal.signal(signal.SIGINT, handle_terminate)


if __name__ == "__main__":
    startup_worker()
    logQueue.put(("Starting logging worker...", logging.INFO))

    # Create a thread object
    speech_thread: threading.Thread = threading.Thread(target=speech_processing_worker)
    image_thread: threading.Thread = threading.Thread(target=image_processing_worker)
    logging_thread: threading.Thread = threading.Thread(target=logging_worker)

    # Start the thread
    logging_thread.start()
    speech_thread.start()
    image_thread.start()
    audio_thread.start()

    # Wait for threads to finish
    speech_thread.join()
    image_thread.join()
    logging_thread.join()
