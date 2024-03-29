# Copyright David Joffe 2024
# Stable diffusion automatic1111 API helper client
import json
import requests
import io
import os
import base64
import datetime
import sys
from PIL import Image, PngImagePlugin

# todo make these configurable either as parameters or other methods
# todo2 wrap the primary functionality in a function so we can reuse elsewhere
#url = "http://127.0.0.1:7860"
#url = "http://davids-mac-mini:7861"
url = "http://10.0.0.10:7861"

payload = {
    "prompt": "puppy dog",
    "negative_prompt": "ugly,nsfw,bad hands,ugly face,low detail,low quality,bad anatomy",
    "steps": 35,
    "seed": -1,
    "width": 512,
    "height": 512,
    "sampler_index": "Euler a",
}

# Check if command line parameter 1 has been passed if so set the payload prompt from it:
if len(sys.argv) > 1:
    payload["prompt"] = sys.argv[1]



print(f'=== URL:{url}/sdapi/v1/txt2img')
response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload)

r = response.json()

for i in r['images']:
    image = Image.open(io.BytesIO(base64.b64decode(i.split(",",1)[0])))

    png_payload = {
        "image": "data:image/png;base64," + i
    }
    response2 = requests.post(url=f'{url}/sdapi/v1/png-info', json=png_payload)

    pnginfo = PngImagePlugin.PngInfo()
    pnginfo.add_text("parameters", response2.json().get("info"))

    # Generate filename based on prompt
    #prompt_filename = "output " + payload["prompt"] + ".png"
    prompt_filename = payload["prompt"] + ".png"

    # Replace invalid chars with space
    prompt_filename = "".join(c if c not in r'\/:*?"<>|' else " " for c in prompt_filename)

    #prompt_filename = prompt_filename.replace(" ", "_")  # Replace spaces with underscores
    prompt_filename = " ".join(prompt_filename.split())  # Remove double spaces
    
    #current_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
    #prompt_filename = current_datetime + "_" + prompt_filename

    if not os.path.exists('output'):
        os.makedirs('output')
    output_folder = datetime.datetime.now().strftime('output/%Y-%m-%d')
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    output_path = os.path.join(output_folder, prompt_filename)
    # Check if output file exists already and if so append a number like " (1).png"
    count = 1
    while os.path.exists(output_path):
        filename, file_extension = os.path.splitext(output_path)
        output_path = f"{filename} ({count}){file_extension}"
        count += 1

    # Add prompt and negative_prompt to PNG metadata
    pnginfo.add_text("prompt", payload["prompt"])
    pnginfo.add_text("negative_prompt", payload["negative_prompt"])
    # Add whole payload as JSON string called Parameters to the PNG
    pnginfo.add_text("Parameters", json.dumps(payload))
    
    image.save(output_path, format='PNG', optimize=True, compress_level=9, pnginfo=pnginfo)
    #image.save('output.png', pnginfo=pnginfo)

    #image.save(prompt_filename, pnginfo=pnginfo)
    #image.save('output.png', pnginfo=pnginfo)