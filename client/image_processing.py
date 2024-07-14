import cv2

video_capture: cv2.VideoCapture = None


# TODO: Add Documentation
def load_image_capture():
    global video_capture
    video_capture = cv2.VideoCapture(0)


# TODO: Add Documentation
def get_image_from_webcam():
    global video_capture
    ret, frame = video_capture.read()
    video_capture.release()
    if not ret:
        raise Exception("Unable to capture image from camera")
    return cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 90])
