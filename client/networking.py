import requests

URL = "https://desktop-gvg2hfa.tail23d4c9.ts.net/process_image"


def upload_image(image, prompt="caption en"):
    response = requests.post(URL, files={"image": image}, data={"prompt": prompt})
    if response.status_code == 200:
        print(
            "Image uploaded and processed successfully!, response: ",
            response.json()["caption"],
        )
    else:
        print(f"Error: Status code {response.status_code} as {response.text}")
    return response
