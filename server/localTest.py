import time
from transformers import AutoProcessor, PaliGemmaForConditionalGeneration
from PIL import Image
import requests
import torch

# Model and Processor Initialization (outside the function to exclude from the run time)
model_id = "google/paligemma-3b-ft-ocrvqa-224"
model = PaliGemmaForConditionalGeneration.from_pretrained(model_id).eval()
processor = AutoProcessor.from_pretrained(model_id)

def model_run(url="https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/transformers/tasks/car.jpg?download=true"):    
    # Start timing
    start_time = time.time()

    # Measure time to download and load the image
    start_image_time = time.time()
    image = Image.open(requests.get(url, stream=True).raw)
    end_image_time = time.time()

    # Measure time to process the inputs
    start_processing_time = time.time()
    prompt = "caption en"
    model_inputs = processor(text=prompt, images=image, return_tensors="pt")
    input_len = model_inputs["input_ids"].shape[-1]
    end_processing_time = time.time()

    # Measure time to generate the output
    start_generation_time = time.time()
    with torch.inference_mode():
        generation = model.generate(**model_inputs, max_new_tokens=100, do_sample=False)
        generation = generation[0][input_len:]
        decoded = processor.decode(generation, skip_special_tokens=True)
    end_generation_time = time.time()

    # Stop timing
    end_time = time.time()

    # Output the generated caption
    print("Generated Caption:", decoded)

    # Print out timing information
    print(f"Total Execution Time: {end_time - start_time:.2f} seconds")
    print(f"Image Download and Load Time: {end_image_time - start_image_time:.2f} seconds")
    print(f"Input Processing Time: {end_processing_time - start_processing_time:.2f} seconds")
    print(f"Caption Generation Time: {end_generation_time - start_generation_time:.2f} seconds")

# Run the performance test
model_run("https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/transformers/tasks/car.jpg?download=true") 
