import requests

from image_processing import get_image_from_webcam

URL = "http://localhost:5000/process_image"


def upload_image(image):
    response = requests.post(URL, files={"image": image})
    if response.status_code == 200:
        print(
            "Image uploaded and processed successfully!, response: ",
            response.json()["caption"],
        )
    else:
        print(f"Error: Status code {response.status_code} as {response.text}")
    return response
