import json
import os

with open("images.json", "r") as f:
    images = json.load(f)

for image_name, image_url in images.items():
    os.system(f"docker pull {image_url}")
    if "@" in image_url:
        image_url = image_url.split("@")[0]
    os.system(f"docker inspect {image_url} > {image_name}/inspect.json")
    os.system("python add_image.py {} {}".format(image_name, image_url))
