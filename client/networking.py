import requests
from gps import load_gps, get_gps

URLS = ["https://desktop-gvg2hfa.tail23d4c9.ts.net/","https://laptop-7dmbbhmj.tail23d4c9.ts.net/"]

def discover_server():
    for url in URLS:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print(f"Server found at {url}")
                return url
        except:
            pass
    raise Exception("No servers found, Check your internet connection and try again")

URL = discover_server()
load_gps()

def upload_image(image, prompt="caption en", id="test_id"):
    response = requests.post(URL + "process_image", files={"image": image}, data={
        "prompt": prompt,
        "gps" : get_gps(),
        "id": id
        })
    if response.status_code == 200:
        print(
            "Image uploaded and processed successfully!, response: ",
            response.json()["caption"],
        )
    else:
        print(f"Error: Status code {response.status_code} as {response.text}")
    return response
