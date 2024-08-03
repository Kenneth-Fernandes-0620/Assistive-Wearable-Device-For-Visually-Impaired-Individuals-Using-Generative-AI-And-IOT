from cv2 import VideoCapture, imencode, IMWRITE_JPEG_QUALITY

video_capture: VideoCapture = None


# TODO: Add Documentation
def load_image_capture():
    global video_capture
    video_capture = VideoCapture(0)


# TODO: Add Documentation
def get_image_from_webcam():
    global video_capture
    ret, frame = video_capture.read()
    if not ret:
        raise Exception("Unable to capture image from camera")
    return imencode(".jpg", frame, [IMWRITE_JPEG_QUALITY, 90])


def free_video_capture():
    video_capture.release()


def list_cameras():
    camera_index = 0
    cap = VideoCapture(camera_index)
    if cap.read()[0]:
        print(f"Camera {camera_index} is available")
    else:
        print(f"Camera {camera_index} is not available")
    cap.release()

if __name__ == "__main__":
    list_cameras()