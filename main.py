import threading
import time
from queue import Queue
from cv2.typing import MatLike
from typing import List

from audio_processing import SpeechToText, audio_load, SpeakText
from image_processing import get_image_from_webcam, model_load, image_captioning
from util import measure_time

messageQueue: Queue = None
isRunning: bool = False

commands: List[str] = [
    "describe environment",
    "SOS",
    "help",
]


# TODO: Add Documentation
def startup_worker():  # Function to load the model and audio and initialize the message queue and isRunning flag
    global messageQueue, isRunning

    messageQueue = Queue()
    isRunning = True

    model_load()
    audio_load()


# TODO: Add Documentation
def image_processing_worker():
    global isRunning
    try:
        # wait for queue to contain data, if empty, sleep for 2 seconds
        while isRunning:
            if not messageQueue.empty():
                message: str = messageQueue.get()
                print("Message received from user: ", message)
                if message == commands[0]:
                    image: MatLike = get_image_from_webcam()
                    print("Processing image...")
                    result, time_taken = measure_time(image_captioning, image)
                    print(f"Function result: {result}")
                    print(f"Time taken: {time_taken:.4f} seconds")
                    print(f"End Time: {time.time()}")
                    SpeakText(result)
                elif message == commands[1] or message == commands[2]:                    
                    print("Sending SOS signal...")
                    raise Exception("Unimplemented command: SOS or help")
            else:
                time.sleep(2)
    except Exception as e:
        print(f"Error in image processing worker: {e}")
        isRunning = False


# TODO: Add Documentation
def audio_processing_worker():
    global isRunning
    try:
        while isRunning:
            result: str = SpeechToText()
            if result != None:
                print(f"User said: {result}")
                messageQueue.put(result.lower().strip())
    except Exception as e:
        print(f"Error in audio processing worker: {e}")
        isRunning = False


if __name__ == "__main__":
    startup_worker()

    # Create a thread object
    audio_thread: threading.Thread = threading.Thread(target=audio_processing_worker)
    image_thread: threading.Thread = threading.Thread(target=image_processing_worker)

    # Start the thread
    audio_thread.start()
    image_thread.start()

    # wait for thread1 to finish
    audio_thread.join()
    image_thread.join()

    print("Application finished successfully.")
