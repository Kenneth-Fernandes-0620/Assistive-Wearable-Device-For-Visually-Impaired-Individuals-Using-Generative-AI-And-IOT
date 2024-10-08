import logging
import signal
import threading
import time
from queue import Queue
from typing import List, Optional
import difflib

from audio_processing import capture_speech, load_speech_capture, SpeakText
from util import load_logger
from image_processing import (
    free_image_capture,
    get_image_from_webcam,
    load_image_capture,
    get_QRCode_from_webcam,
)
from networking import getWeather, notifyHelp, upload_image
from similarity_processing import find_most_similar_command

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
    "setup",
    "detect crowd",
    "exit",
    "weather",
]

delay = 0
account_id = "Byi1c2jSuMXSsH958F1ch3TbnLD3"

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
                    # Describe Environment
                    print("Test: Describe Environment")
                    success, image = get_image_from_webcam()
                    print("Got image: ", success)
                    if not success:
                        logQueue.put(
                            ("Unable to capture image from camera", logging.ERROR)
                        )
                        raise Exception("Unable to capture image from camera")
                    else:
                        logQueue.put(("Captured image from camera", logging.INFO))
                    try:
                        response = upload_image(image, "Describe the contents of the Image in English")
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
                    # SOS Signal
                    notifyHelp(account_id)
                    logQueue.put(("Sending SOS signal...", logging.INFO))
                    resultQueue.put(
                        "Sorry, I am unable to send SOS signals at this time"
                    )

                elif message == commands[3]:
                    # Setup device
                    result = get_QRCode_from_webcam()
                    logQueue.put((f"QR Code Scanned: {result}", logging.INFO))
                    resultQueue.put(f"QR Code Detected, will attempt to setup")

                elif message == commands[4]:
                    # Crowd Detection
                    success, image = get_image_from_webcam()
                    if not success:
                        logQueue.put(
                            ("Unable to capture image from camera", logging.ERROR)
                        )
                        raise Exception("Unable to capture image from camera")
                    else:
                        logQueue.put(("Captured image from camera", logging.INFO))
                    try:
                        response = upload_image(
                            image, "Does the image contain a crowed of people?"
                        )
                        response_json = response.json()
                        detections = response_json.get("caption", [])
                        print("detected: ", detections)
                        logQueue.put(
                            (f"Received response: {response_json}", logging.INFO)
                        )
                    except Exception as e:
                        logQueue.put(
                            (f"Error in uploading image, {e.args[0]}", logging.ERROR)
                        )
                        resultQueue.put(
                            "Sorry, I am having trouble uploading the image. Please check your internet connection and try again"
                        )
                elif message == commands[5]:
                    # Exit
                    logQueue.put(("Exiting...", logging.INFO))
                    resultQueue.put("Goodbye!")
                    isRunning = False

                elif message == commands[6]:
                    result = getWeather()
                    resultQueue.put(result)
                isWaiting = False
            else:
                time.sleep(0.5)
    except Exception as e:
        print(e.args[0])
        logQueue.put((f"Error in image processing worker: {e.args[0]}", logging.ERROR))
        isRunning = False
    free_image_capture()


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
                    print(f"I heard: {result}")
                    # command = find_most_similar_command(result)
                    command = find_most_similar_command(result)
                    print(f"Command: {command}")
                    if command is not None:
                        print("Waiting...")
                        resultQueue.put("I have received the command to " + command)
                        messageQueue.put(command)
                        logQueue.put(("Message received from user.", logging.INFO))
                        isWaiting = True
            if isWaiting:
                time.sleep(0.1)
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
    speech_thread: threading.Thread = threading.Thread(
        target=speech_processing_worker
    )  # Does Speech Recognition
    image_thread: threading.Thread = threading.Thread(
        target=image_processing_worker
    )  # Does Image capture and Processing
    logging_thread: threading.Thread = threading.Thread(
        target=logging_worker
    )  # Logs messages
    audio_thread: threading.Thread = threading.Thread(
        target=audio_processing_worker
    )  # Does Audio Output

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
