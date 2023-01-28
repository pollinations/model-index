"""
Updates images.json

Usage: python add_image.py <image_name> <image_url>
"""
import json
import sys
import time
import os

image_name = sys.argv[1]
original_url = sys.argv[2]
image_url = original_url.split("@")[0]

with open("images.json", "r") as f:
    images = json.load(f)

images[sys.argv[1]] = sys.argv[2]

with open("images.json", "w") as f:
    json.dump(images, f, indent=4)

with open("metadata.json", "r") as f:
    metadata = json.load(f)

ok = False
while not ok:
    # try:
        with open(f"{image_name}/inspect.json", "r") as f:
            inspect = json.load(f)
            assert len(inspect) > 0
            try:
                openapi = json.loads(inspect[0]["ContainerConfig"]["Labels"]["org.cogmodel.openapi_schema"])
                hash = inspect[0]["Id"]
            except:
                openapi = json.loads(inspect[0]["Config"]["Labels"]["org.cogmodel.openapi_schema"])

            hash = inspect[0]["Id"]
            ok = True
    # except:
    #     os.system(f"docker pull {original_url}")
    #     time.sleep(5)
    #     os.system(f"docker inspect {original_url} > {image_name}/inspect.json")
    #     time.sleep(5)

try:
    with open(f"{image_name}/meta.json", "r") as f:
        meta = json.load(f)
except Exception as e:
    print(e)
    meta = {}


metadata[image_url] = {
    "hash": hash,
    "full_url": f"{image_url}@{hash}",
    "openapi": openapi,
    "meta": meta
}

with open("metadata.json", "w") as f:
    metadata = json.dump(metadata, f, indent=4)
