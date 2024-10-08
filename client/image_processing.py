from threading import Thread
import time
from cv2 import VideoCapture, QRCodeDetector, cvtColor, imencode, IMWRITE_JPEG_QUALITY, COLOR_BGR2GRAY

# video_capture: VideoCapture = None

# TODO: Add Documentation
def load_image_capture():
    # global video_capture
    # video_capture = VideoCapture(0)
    # video_capture.read() # initial read to get the camera started
    pass


# TODO: Add Documentation
def get_image_from_webcam():
    # global video_capture
    video_capture = VideoCapture(0)
    print("Getting image from webcam")

    if video_capture is None:
            raise Exception("Video capture is not initialized. Call load_image_capture first.")

    video_capture.read() # initial read to get the camera started
    time.sleep(1)
    ret, frame = video_capture.read()
    if not ret:
        raise Exception("Unable to capture image from camera")
    
    video_capture.release()
    return imencode(".jpg", frame, [IMWRITE_JPEG_QUALITY, 90])


def free_image_capture():
    """Releases the video capture object."""
    # global video_capture
    # if video_capture is not None:
    #     video_capture.release()
    #     video_capture = None



def list_cameras():
    camera_index = 0
    cap = VideoCapture(camera_index)
    if cap.read()[0]:
        print(f"Camera {camera_index} is available")
    else:
        print(f"Camera {camera_index} is not available")
    cap.release()

def get_QRCode_from_webcam() -> str:
    global video_capture
    ret, frame = video_capture.read()
    if not ret:
        raise Exception("Unable to capture image from camera")
    data, bbox, _ = QRCodeDetector().detectAndDecode(
        cvtColor(frame, COLOR_BGR2GRAY)
    )

    return data

if __name__ == "__main__":
    list_cameras()
    load_image_capture()
    while True:
        res = get_QRCode_from_webcam()
        if res:
            print(res)
            break