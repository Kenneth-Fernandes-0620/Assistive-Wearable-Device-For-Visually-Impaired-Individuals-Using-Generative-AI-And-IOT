import threading
import time
from queue import Queue
from typing import List

from audio_processing import (
    SpeechToText,
)
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


# TODO: Add Documentation
def startup_worker():  # Function to load the model and audio and initialize the message queue and isRunning flag
    global messageQueue, resultQueue, isRunning, isWaiting

    messageQueue = Queue()
    resultQueue = Queue()

    isRunning = True


# TODO: Add Documentation
def image_processing_worker():
    global isRunning, isWaiting
    try:
        # wait for queue to contain data, if empty, sleep for 2 seconds
        while isRunning:
            if not messageQueue.empty():
                message: str = messageQueue.get()
                print("Message received from user: ", message)
                if message == commands[0]:
                    success, image = get_image_from_webcam()
                    if not success:
                        raise Exception("Unable to capture image from camera")
                    print("Processing image...")
                    result = upload_image(image)
                    resultQueue.put(result.json()["caption"])
                    print("Queue size: ", resultQueue.qsize())
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


# TODO: Add Documentation
def speech_processing_worker():
    global isRunning, isWaiting
    try:
        while isRunning:
            while not isWaiting:
                result: str = SpeechToText()
                if result != None and result.lower().strip() in commands:
                    messageQueue.put(result.lower().strip())
                    isWaiting = True
            if isWaiting:
                time.sleep(2)
    except Exception as e:
        print(f"Error in audio processing worker: {e}")
        isRunning = False


if __name__ == "__main__":
    startup_worker()

    # Create a thread object
    speech_thread: threading.Thread = threading.Thread(target=speech_processing_worker)
    image_thread: threading.Thread = threading.Thread(target=image_processing_worker)

    # Start the thread
    speech_thread.start()
    image_thread.start()

    # wait for thread1 to finish
    speech_thread.join()
    image_thread.join()

    print("Application finished successfully.")
