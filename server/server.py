from flask import Flask, request, jsonify, send_from_directory
import cv2
import numpy as np

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

    if "image" not in request.files:
        return jsonify({"error": "No image file uploaded"}), 400

    elif prompt == "":
        return jsonify({"error": "No prompt provided"}), 400

    try:
        # Get the image file
        image_file = request.files["image"].read()
        decoded_image: cv2.typing.MatLike = cv2.imdecode(
            np.fromstring(image_file, np.uint8), cv2.IMREAD_COLOR
        )
        recolored_image: cv2.typing.MatLike = cv2.cvtColor(
            decoded_image, cv2.COLOR_BGR2RGB
        )
        try:
            return jsonify({"caption": image_captioning(recolored_image, prompt)}), 200
        except Exception as e:
            print(f"Error processing image: {e}")
            return jsonify({"error": f"Error processing image: {e}"}), 500

    except Exception as e:
        print(f"Error processing image: {e}")
        return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    app.run()
