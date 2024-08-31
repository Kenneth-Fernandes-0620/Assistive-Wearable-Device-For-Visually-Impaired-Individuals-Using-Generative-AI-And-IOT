import os
import requests
from gps import dms_to_dd, load_gps, get_gps

URLS = [
    "https://desktop-gvg2hfa.tail23d4c9.ts.net/",
    "https://laptop-7dmbbhmj.tail23d4c9.ts.net/",
]
WEATHER_API_KEY = "9f8fa3a83ebf44daa41131159242908"
BASE_WEATHER_URL = "http://api.weatherapi.com/v1"
CURRENT_WEATHER_URL = BASE_WEATHER_URL + "/current.json"


def discover_server():
    """
    Discover an available server from a list of URLs.

    :return: URL of the available server
    :raises Exception: If no servers are found
    """
    for url in URLS:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print(f"Server found at {url}")
                return url
        except requests.exceptions.RequestException as e:
            print(f"Server not reachable at {url}, Error: {e}")
            continue
    raise Exception("No servers found. Check your internet connection and try again.")


# Discover available server
URL = discover_server()


def upload_image(image, prompt="caption en", id="test_id"):
    response = requests.post(
        URL + "process_image",
        files={"image": image},
        data={"prompt": prompt, "gps": get_gps(), "id": id},
    )
    if response.status_code == 200:
        print(
            "Image uploaded and processed successfully!, response: ",
            response.json()["caption"],
        )
    else:
        print(f"Error: Status code {response.status_code} as {response.text}")
    return response


def upload_image_test(image_path, prompt="caption en", gps="0,0", user_id="test_id"):
    """
    Upload an image to the server with additional data like manually entered GPS coordinates and an ID.

    :param image_path: Path to the image file
    :param prompt: Prompt to send along with the image
    :param gps: Manually entered GPS coordinates
    :param user_id: Custom identifier for the image
    :return: Server response
    """
    with open(image_path, "rb") as image_file:
        print(f"Trying to make request to {URL}process_image ")
        response = requests.post(
            URL + "process_image",
            files={"image": image_file},
            data={
                "prompt": prompt,
                "gps": gps,  # Manually entered GPS coordinates
                "id": user_id,  # Manually entered image ID
            },
        )
        if response.status_code == 200:
            caption = response.json().get("caption", "No caption provided")
            print(
                f"Image '{os.path.basename(image_path)}' uploaded and processed successfully! Response: {caption}"
            )
            return caption
        else:
            print(
                f"Error uploading image '{os.path.basename(image_path)}': Status code {response.status_code} - {response.text}"
            )
            return None

def notifyHelp(uid: str = ""):
    response = requests.get(URL + "help",params={"id": uid})
    if response.status_code == 200:
        print("Help requested successfully!")
    else:
        print(f"Error: Status code {response.status_code} as {response.text}")
    return response

def getWeather(location: str = dms_to_dd(get_gps())):
    print(f"Hitting Api: {CURRENT_WEATHER_URL} with data {location}")
    response = requests.get(
        CURRENT_WEATHER_URL, params={"q": location, "key": WEATHER_API_KEY}
    )
    if response.status_code == 200:
        # print(f"Weather at {location}: {response.json()}")/
        pass
    else:
        print(f"Error: Status code {response.status_code} as {response.text}")
        return "Error fetching weather data"
    data: dict = response.json()
    current = data.get("current")

    condition = current.get("condition") if current else None

    humidity = current.get("humidity") if current else None
    feelslike_c = current.get("feelslike_c") if current else None
    return (
        f"Humidity is {humidity}%, {condition.get('text')}, Feels like {feelslike_c} °C"
    )


def process_images_in_folder(
    folder_path, prompt="caption en", gps="0,0", user_id="test_id"
):
    """
    Process all images in a specified folder by uploading them to the server.

    :param folder_path: Path to the folder containing images
    :param prompt: Custom prompt to send with each image
    :param gps: Manually entered GPS coordinates
    :param user_id: Custom identifier for the image
    :return: List of tuples containing image name and response from the server
    """
    responses = []

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        if filename.lower().endswith((".jpg", ".jpeg", ".png")):
            print(f"Processing image: {filename}")
            response = upload_image_test(
                file_path, prompt=prompt, gps=gps, user_id=user_id
            )
            if response is not None:
                responses.append((filename, response))
        else:
            print(f"Skipping non-image file: {filename}")

    return responses


def main():
    # Specify the base path to the folder containing images
    base_folder_path = "E:\\Assistive-Wearable-Device-For-Visually-Impaired-Individuals-Using-Generative-AI-And-IOT\\client\\test_images"

    # Get the custom prompt and other inputs from the user
    custom_prompt = input("Enter a custom prompt for image processing: ")
    latitude = input("Enter the latitude: ")
    longitude = input("Enter the longitude: ")
    manual_gps = f"{latitude},{longitude}"
    user_id = input("Enter a custom ID for the images: ")

    # Get the user's choice for the folder
    choice = input(
        "Enter '1' to process images from 'sorrounding' folder or '2' to process images from 'crowd' folder: "
    )

    if choice == "1":
        folder_path = os.path.join(base_folder_path, "sorrounding")
    elif choice == "2":
        folder_path = os.path.join(base_folder_path, "crowd")
    else:
        print("Invalid choice. Exiting.")
        return

    if not os.path.isdir(folder_path):
        print(f"Folder not found: {folder_path}")
        return

    all_responses = process_images_in_folder(
        folder_path, prompt=custom_prompt, gps=manual_gps, user_id=user_id
    )

    for image_name, caption in all_responses:
        print(f"Image: {image_name}, Caption: {caption}")


if __name__ == "__main__":
    print("Testing weather API")
    print(getWeather(dms_to_dd(get_gps())))
