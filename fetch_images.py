import json
import sys


with open("images.json", "r") as f:
    images = json.load(f)

for _, image in images.items():
    print(f"docker pull {image}")
    if "@" in image:
        print(f"docker tag {image} {image.split('@')[0]}")