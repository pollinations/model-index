"""
Updates images.json

Usage: python add_image.py <image_name> <image_url>
"""
import json
import sys


with open("images.json", "r") as f:
    images = json.load(f)

images[sys.argv[1]] = sys.argv[2]

with open("images.json", "w") as f:
    json.dump(images, f, indent=4)
