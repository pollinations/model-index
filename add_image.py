"""
Updates images.json

Usage: python add_image.py <image_name> <image_url>
"""
import json
import sys

image_name = sys.argv[1]
image_url = sys.argv[2]

with open("images.json", "r") as f:
    images = json.load(f)

images[sys.argv[1]] = sys.argv[2]

with open("images.json", "w") as f:
    json.dump(images, f, indent=4)

with open("metadata.json", "r") as f:
    metadata = json.load(f)

with open(f"{image_name}/inspect.json", "r") as f:
    inspect = json.load(f)

try:
    with open(f"{image_name}/meta.json", "r") as f:
        meta = json.load(f)
except:
    meta = {}

openapi = inspect[0]["ContainerConfig"]["Labels"]["org.cogmodel.openapi_schema"]
hash = inspect[0]["Id"]

metadata[image_url] = {
    "hash": hash,
    "full_url": f"{image_url}@{hash}",
    "openapi": openapi,
    "meta": meta
}

with open("metadata.json", "w") as f:
    metadata = json.dump(metadata, f, indent=4)
