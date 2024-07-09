import time
from transformers import AutoProcessor, PaliGemmaForConditionalGeneration
from PIL import Image
import torch
import cv2
import numpy as np

from util import measure_time

model_id: str = "google/paligemma-3b-mix-224"
model: PaliGemmaForConditionalGeneration = None
processor: AutoProcessor = None
prompt: str = "caption en"


# TODO: Add Documentation
def model_load():
    global model, processor
    model = PaliGemmaForConditionalGeneration.from_pretrained(model_id).eval()
    processor = AutoProcessor.from_pretrained(model_id)


# TODO: Add Documentation
def image_captioning(url: str):
    if model is None or processor is None:
        raise Exception("Model not loaded, call model_load() first.")

    model_inputs = processor(text=prompt, images=Image.open(url), return_tensors="pt")
    input_len = model_inputs["input_ids"].shape[-1]

    with torch.inference_mode():
        generation = model.generate(**model_inputs, max_new_tokens=100, do_sample=False)
        generation = generation[0][input_len:]
        return processor.decode(generation, skip_special_tokens=True)


# TODO: Add Documentation
def image_captioning(image: np.ndarray):
    if model is None or processor is None:
        raise Exception("Model not loaded, call model_load() first.")

    model_inputs = processor(
        text=prompt, images=Image.fromarray(image), return_tensors="pt"
    )
    input_len = model_inputs["input_ids"].shape[-1]

    with torch.inference_mode():
        generation = model.generate(**model_inputs, max_new_tokens=100, do_sample=False)
        generation = generation[0][input_len:]
        return processor.decode(generation, skip_special_tokens=True)


# TODO: Add Documentation
def get_image_from_webcam() -> cv2.typing.MatLike:
    cap = cv2.VideoCapture(0)
    time.sleep(2)  # wait for a second to let the camera adjust to the light
    ret, frame = cap.read()
    if not ret:
        raise Exception("Unable to capture image from camera")
    cap.release()
    return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # Convert to RGB format for PIL

# Code for testing the image captioning function
if __name__ == "__main__":
    frame = get_image_from_webcam()
    model_load()
    print(f"Start Time: {time.time()}")
    # url = "./test_images/car.jpg"
    result, time_taken = measure_time(image_captioning, frame)
    print(f"Function result: {result}")
    print(f"Time taken: {time_taken:.4f} seconds")
    print(f"End Time: {time.time()}")
