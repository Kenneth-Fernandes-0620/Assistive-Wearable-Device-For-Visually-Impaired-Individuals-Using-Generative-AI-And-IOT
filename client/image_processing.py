import time
import cv2


def get_image_from_webcam():
    cap = cv2.VideoCapture(0)
    time.sleep(2)  # wait for a second to let the camera adjust to the light
    ret, frame = cap.read()
    if not ret:
        raise Exception("Unable to capture image from camera")
    cap.release()
    return cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 90])
