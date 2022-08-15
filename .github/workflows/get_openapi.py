import json
import os


with open("images.json", "r") as f:
    images = json.load(f)


def system(cmd):
    print(f"Running: {cmd}")
    print("Exit status: ", os.system(cmd))


def get_openapi(path, image):
    print("Get: ", path, image)
    if "amazonaws" in image:
        print("Skip: ", path, image)
        return #private registry, repo ci is responsible for generting openapi.json
    #system("docker system prune -af")
    system(f"docker pull {image}")
    system(f"docker inspect {image} > {path}/inspect.json")


for path, image in images.items():
    all_openapi_jsons = {}
    if not os.path.exists(path):
        all_openapi_jsons[image] = get_openapi(path, image)
        os.system(f"python add_image.py {path} {image}")