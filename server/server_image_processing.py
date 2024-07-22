from transformers import AutoProcessor, PaliGemmaForConditionalGeneration
from PIL import Image
import torch
import numpy as np

model_id: str = "google/paligemma-3b-ft-ocrvqa-224"
model: PaliGemmaForConditionalGeneration = None
processor: AutoProcessor = None
prompt: str = "caption en"

MODEL_DIR = "model"
AUTOPROCESSOR_DIR = "autoprocessor"


def model_save():
    global model, processor
    if not model or not processor:
        raise Exception("Model not loaded, call model_load() first.")
    model.save_pretrained(f"{MODEL_DIR}/{model_id}", from_pt=True)
    processor.save_pretrained(f"{AUTOPROCESSOR_DIR}/{model_id}")


# TODO: Add Documentation
def model_load():
    global model, processor

    try:
        model = PaliGemmaForConditionalGeneration.from_pretrained(
            f"{MODEL_DIR}/{model_id}"
        ).eval()
        processor = AutoProcessor.from_pretrained(f"{AUTOPROCESSOR_DIR}/{model_id}")
        print(f"Model loaded from local system")
    except OSError:
        print(f"Could not load model from local system")
        model = PaliGemmaForConditionalGeneration.from_pretrained(model_id).eval()
        processor = AutoProcessor.from_pretrained(model_id)
        model_save()  # Save the model to the local system


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


# To save the model, run this script as a standalone script
if __name__ == "__main__":
    model_load()
    model_save()
