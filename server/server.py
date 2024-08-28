from flask import Flask, request, jsonify, send_from_directory
import cv2
import numpy as np
import os

from firebase_helper import send_document_to_firestore
from server_image_processing import image_captioning, model_load


model_load()
print("Model loaded successfully")

app = Flask(__name__)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(app.static_folder, 'favicon.ico')

# Routes
@app.route("/")
def health_check():
    return "ok", 200


@app.route("/process_image", methods=["POST"])
def process_image():

    # Check if image file is present in the request
    prompt = request.form.get("prompt","")
    uid = request.form.get("id","")
    gps = request.form.get("gps","")

    if "image" not in request.files:
        return jsonify({"error": "No image file uploaded"}), 400

    elif prompt == "":
        return jsonify({"error": "No prompt provided"}), 400


    print(f"Processing image with prompt: {prompt}, for user: {uid}, with gps: {gps}")

    try:
        image_contents = request.files["image"]
        image_file = image_contents.read()

        # Enable the following code to save the image to the local drive
        # Save the image to the local drive
        image_path = os.path.join("images", "res.jpg")
        with open(image_path, "wb") as f:
            f.write(image_file)

        decoded_image: cv2.typing.MatLike = cv2.imdecode(
            np.fromstring(image_file, np.uint8), cv2.IMREAD_COLOR
        )
        recolored_image: cv2.typing.MatLike = cv2.cvtColor(
            decoded_image, cv2.COLOR_BGR2RGB
        )
        try:
            result = image_captioning(recolored_image, prompt)
            if uid != "":
                send_document_to_firestore("requests", {"uid": uid, "prompt": prompt, "result": result, "gps": gps})
            return jsonify({"caption": result}), 200
        except Exception as e:
            print(f"Error processing image: {e}")
            if uid != "":
                send_document_to_firestore("errors", {"uid": uid, "prompt": prompt, "error": f"Error processing image: {e}"})
            return jsonify({"error": f"Error processing image: {e}"}), 500

    except Exception as e:
        print(f"Error processing image: {e}")
        if uid != "":
            send_document_to_firestore("errors", {"uid": uid, "prompt": prompt, "error": f"Error processing image: {e}"})
        return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    app.run()
