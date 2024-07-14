import signal
import threading
import time
from queue import Queue
from typing import List, Optional
import spacy

from audio_processing import SpeechToText, TTSEngine, SpeakText, startTTSEngine
from image_processing import get_image_from_webcam
from networking import upload_image

messageQueue: Queue = None
resultQueue: Queue = None
isRunning: bool = False
isWaiting: bool = True

commands: List[str] = [
    "describe environment",
    "SOS",
    "help",
]

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

def startup_worker():
    global messageQueue, resultQueue, isRunning, isWaiting

    messageQueue = Queue()
    resultQueue = Queue()

    isRunning = True
    isWaiting = False

    TTSEngine()    


# TODO: Add Documentation
def text_to_speech_worker():
    startTTSEngine()

def image_processing_worker():
    global isRunning, isWaiting
    try:
        while isRunning:
            if not messageQueue.empty():
                message: str = messageQueue.get()
                print("Message received from user: ", message)
                if message == commands[0]:
                    res, image = get_image_from_webcam()
                    if not res:
                        raise Exception("Unable to capture image from camera")
                    print("Processing image...")
                    result = upload_image(image)
                    resultQueue.put(result.json()["caption"])
                    SpeakText(result.json()["caption"])
                elif message == commands[1] or message == commands[2]:
                    print("Sending SOS signal...")
                    raise Exception("Unimplemented command: SOS or help")
                print("Image processing complete.")
                isWaiting = False
            else:
                time.sleep(2)
    except Exception as e:
        print(f"Error in image processing worker: {e}")
        isRunning = False

def speech_processing_worker():
    global isRunning, isWaiting
    try:
        while isRunning:
            while not isWaiting:
                speech: str = SpeechToText()
                if speech is not None:
                    messageQueue.put(speech)
                    isWaiting = True
            if isWaiting:
                time.sleep(2)
    except Exception as e:
        print(f"Error in audio processing worker: {e}")
        isRunning = False


if __name__ == "__main__":
    print("Starting application...")
    startup_worker()
    print("Application started successfully.")

    # Create a thread object
    speech_thread: threading.Thread = threading.Thread(target=speech_processing_worker)
    image_thread: threading.Thread = threading.Thread(target=image_processing_worker)
    audio_thread: threading.Thread = threading.Thread(target=text_to_speech_worker)

    # Start the threads
    speech_thread.start()
    image_thread.start()

    while isRunning:
        pass

    # Wait for threads to finish
    speech_thread.join()
    image_thread.join()

    print("Application finished successfully.")
