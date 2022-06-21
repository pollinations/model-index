import json
import os


with open("images.json", "r") as f:
    images = json.load(f)


def system(cmd):
    print(f"Running: {cmd}")
    print("Exit status: ", os.system(cmd, shell=True))


def get_openapi(path, image):
    print("Get: ", path, image)
    if "amazonaws" in image:
        print("Skip: ", path, image)
        return #private registry, repo ci is responsible for generting openapi.json
    system(f"docker pull {image}")
    system(f"docker inspect {image} > inspect.json")
    with open("inspect.json", "r") as f:
        data = json.load(f)[0]
    os.makedirs(path)
    with open(f"{path}/openapi.json", "w") as f:
       f.write(data["ContainerConfig"]["Labels"]["org.cogmodel.openapi_schema"])
    system("rm inspect.json")


for path, image in images.items():
    if not os.path.exists(path):
        get_openapi(path, image)
