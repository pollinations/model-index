import json
import os

def system(cmd):
    print(cmd)
    os.system(cmd)

with open("images.json", "r") as f:
    images = json.load(f)

for image_name, image_url in images.items():
    system("python add_image.py {} {}".format(image_name, image_url))
