import logging
import signal
import threading
import time
from queue import Queue
from typing import List, Optional
import difflib

from audio_processing import (
    capture_speech,
    load_speech_capture,
    SpeakText
)
from util import load_logger
from image_processing import (
    free_video_capture,
    get_image_from_webcam,
    load_image_capture,
)
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
    "exit",
]


def startup_worker():
    global messageQueue, resultQueue, isRunning, isWaiting, logQueue

    messageQueue = Queue()
    resultQueue = Queue()
    logQueue = Queue()

    isRunning = True
    isWaiting = False


def match_command(speech: str) -> Optional[str]:
    """
    This function takes a string input and determines if it matches any of the predefined commands
    using sequence matching.
    If a match is found, it returns the command; otherwise, it returns None.
    """
    speech = speech.lower().strip()
    closest_matches = difflib.get_close_matches(speech, commands, n=1, cutoff=0.75)
    return closest_matches[0] if closest_matches else None


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
                        logQueue.put(
                            (
                                f"Image uploaded successfully and got response: {response.json()['caption']}",
                                logging.INFO,
                            )
                        )
                    except Exception as e:
                        logQueue.put(
                            (f"Error in uploading image, {e.args[0]}", logging.ERROR)
                        )
                        resultQueue.put(
                            "Sorry, I am having trouble uploading the image. Please check your internet connection and try again"
                        )
                elif message == commands[1] or message == commands[2]:
                    logQueue.put(("Sending SOS signal...", logging.INFO))
                    resultQueue.put(
                        "Sorry, I am unable to send SOS signals at this time"
                    )
                    raise Exception("Unimplemented command: SOS or help")
                elif message == commands[3]:
                    logQueue.put(("Exiting...", logging.INFO))
                    resultQueue.put("Goodbye!")
                    isRunning = False
                isWaiting = False
            else:
                time.sleep(0.5)
    except Exception as e:
        print(e.args[0])
        logQueue.put((f"Error in image processing worker: {e.args[0]}", logging.ERROR))
        isRunning = False
    free_video_capture()


def audio_processing_worker():
    while isRunning:        
        if not resultQueue.empty():
            result: str = resultQueue.get()
            SpeakText(result)
            logQueue.put(("Audio output sent.", logging.INFO))
        else:
            time.sleep(0.5)

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


def speech_processing_worker():
    global isRunning, isWaiting, logQueue
    load_speech_capture()
    logQueue.put(("Speech processing worker started.", logging.INFO))
    try:
        while isRunning:
            while not isWaiting:
                result: str = capture_speech()
                if result:
                    print(result)
                    command = match_command(result)
                    if command is not None:
                        resultQueue.put("I have recieved the command to " + command)
                        messageQueue.put(command)
                        logQueue.put(("Message received from user.", logging.INFO))
                        isWaiting = True
            if isWaiting:
                time.sleep(0.5)
    except Exception as e:
        logQueue.put((f"Error in Speech processing worker: {e}", logging.ERROR))
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

    # Create thread objects
    speech_thread: threading.Thread = threading.Thread(target=speech_processing_worker) # Does Speech Recognition
    image_thread: threading.Thread = threading.Thread(target=image_processing_worker) # Does Image capture and Processing
    logging_thread: threading.Thread = threading.Thread(target=logging_worker) # Logs messages
    audio_thread: threading.Thread = threading.Thread(target=audio_processing_worker) # Does Audio Output

    # Start the threads
    logging_thread.start()
    speech_thread.start()
    image_thread.start()
    audio_thread.start()

    # Wait for threads to finish
    speech_thread.join()
    image_thread.join()
    logging_thread.join()
    audio_thread.join()
