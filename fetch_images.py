import json


with open("images.json", "r") as f:
    images = json.load(f)

with open("metadata.json", "r") as f:
    metadata = json.load(f)

try:
    with open("pollinator_group", "r") as f:
        pollinator_group = f.read().strip()
except:
    pollinator_group = "T4"

for _, image in images.items():
    if pollinator_group not in metadata[image.split("@")[0]]["meta"]["pollinator_group"]:
        continue
    print(f"docker pull {image}")
    if "@" in image:
        print(f"docker tag {image} {image.split('@')[0]}")