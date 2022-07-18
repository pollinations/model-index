import json
import sys


with open("images.json", "r") as f:
    images = json.load(f)


all_images_open_api = {}
for path, image in images.items():
    with open(f"{path}/openapi.json", "r") as f:
        open_api = json.load(f)

    all_images_open_api[image] = open_api

with open("images_openapi.json", "w") as f:
    json.dump(all_images_open_api, f, indent=4)