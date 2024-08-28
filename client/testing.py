import os
import requests

# Define the URL for processing images
URL = "https://desktop-gvg2hfa.tail23d4c9.ts.net/process_image"

def upload_image(image_path, prompt="caption en"):
    """
    Upload an image to the server and get the response.

    :param image_path: Path to the image file
    :param prompt: Additional data to send with the image (optional)
    :return: Response from the server
    """
    with open(image_path, "rb") as image_file:
        response = requests.post(URL, files={"image": image_file}, data={"prompt": prompt})
        if response.status_code == 200:
            caption = response.json().get("caption", "No caption provided")
            print(f"Image '{os.path.basename(image_path)}' uploaded and processed successfully! Response: {caption}")
            return caption
        else:
            print(f"Error uploading image '{os.path.basename(image_path)}': Status code {response.status_code} - {response.text}")
            return None

def process_images_in_folder(folder_path, prompt="caption en"):
    """
    Process all images in a specified folder by uploading them to the server.

    :param folder_path: Path to the folder containing images
    :param prompt: Custom prompt to send with each image (optional)
    :return: List of tuples containing image name and response from the server
    """
    # List to store responses with image names
    responses = []
    
    # Loop through all files in the folder
    for filename in os.listdir(folder_path):
        # Construct the full path to the image file
        file_path = os.path.join(folder_path, filename)
        
        # Check if the file is an image (e.g., jpg, jpeg, png)
        if filename.lower().endswith((".jpg", ".jpeg", ".png")):
            print(f"Processing image: {filename}")
            # Upload the image and get the response
            response = upload_image(file_path, prompt)
            # Store the response with the image name in the list
            if response is not None:
                responses.append((filename, response))
        else:
            print(f"Skipping non-image file: {filename}")
    
    return responses

if __name__ == "__main__":
    # Specify the path to the folder containing images
    folder_path = "E:\\Assistive-Wearable-Device-For-Visually-Impaired-Individuals-Using-Generative-AI-And-IOT\\client\\Camera Roll"
     # Custom prompt for processing images
    custom_prompt = input("Enter a custom prompt for image processing: ")
    
    # Call the function to process images and get responses
    all_responses = process_images_in_folder(folder_path, prompt=custom_prompt)
    
    # Print all the responses with image names
    for image_name, caption in all_responses:
        print(f"Image: {image_name}, Caption: {caption}")
