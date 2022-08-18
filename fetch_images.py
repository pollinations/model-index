import json
import os

with open("images.json", "r") as f:
    images = json.load(f)

os.system("curl -o metadata.json https://raw.githubusercontent.com/pollinations/model-index/main/metadata.json")
with open("metadata.json", "r") as f:
    metadata = json.load(f)


pollinator_group = "T4"
with open(".env", "r") as f:
    for line in f.readlines():
        env, val = line.split("=")
        if env == "POLLINATOR_GROUP":
            pollinator_group = val.strip()

print("# Pollinator group:", pollinator_group)  

for _, image in images.items():
    try:
        assert pollinator_group in metadata[image.split("@")[0]]["meta"]["pollinator_group"]
    except (AssertionError, KeyError):
        print("# Ignore ", image)
        continue
    print(f"docker pull {image}")
    if "@" in image:
        print(f"docker tag {image} {image.split('@')[0]}")
