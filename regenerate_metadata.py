import json
import os

def system(cmd):
    print(cmd)
    os.system(cmd)

with open("images.json", "r") as f:
    images = json.load(f)

for image_name, image_url in images.items():
    system(f"docker pull {image_url}")
    if "@" in image_url:
        image_url = image_url.split("@")[0]
    system(f"docker inspect {image_url} > {image_name}/inspect.json")
    system("python add_image.py {} {}".format(image_name, image_url))
