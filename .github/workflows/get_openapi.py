import json
import os


with open("images.json", "r") as f:
    images = json.load(f)


def get_openapi(path, image):
    if "amazonaws" in image:
        return #private registry, repo ci is responsible for generting openapi.json
    os.system(f"docker pull {image}")
    os.system(f"docker inspect {image} > inspect.json", shell=True, )
    with open("inspect.json", "r") as f:
        data = json.load(f)[0]
    os.makedirs(path)
    with open(f"{path}/openapi.json", "w") as f:
       f.write(data["ContainerConfig"]["Labels"]["org.cogmodel.openapi_schema"])
    os.system("rm inspect.json")


for path, image in images.items():
    if not os.path.exists(path):
        get_openapi(path, image)
