"""
This script is pulled and executed every 5min on the workers and is used to bring the instance into a desired state
"""
import json
import os

home_dir = "/home/ec2-user"
if not os.path.exists(home_dir):
    home_dir = "/home/nielswarncke"
if not os.path.exists(home_dir):
    home_dir = "/home/ubuntu"

os.system("rm /tmp/fetch.log")

def log(msg):
    with open("/tmp/fetch.log", "a") as f:
        f.write(f"{msg}\n")

def sudo(cmd):
    system(f"sudo {cmd}")


def system(cmd):
    if "docker pull" in cmd:
        breakpoint()
    log("-"*80)
    log(cmd)
    result = os.popen(cmd).read()
    log(result)
    log("-"*80)

    
gpu_flag = "--gpus all" if sudo("nvidia-smi  > /dev/null 2>&1") == 0 else ""

with open(f"{home_dir}/pull_updates_and_restart.sh", "r") as f:
    content = f.read()
    dev_or_main = "dev" if "pollinator:dev" in content else "main"

sudo("echo 1 >> /tmp/log")
sudo(f"echo  gpu_flag={gpu_flag} dev_or_main={dev_or_main} home_dir={home_dir}>> /tmp/log")


sudo(f"chmod a+w {home_dir}/pull_updates_and_restart.sh")

sudo("crontab -r  ")
sudo("crontab -l > fetch_updates")
sudo(f'echo "*/5 * * * * /bin/bash {home_dir}/pull_updates_and_restart.sh" >> fetch_updates')
sudo(f'echo "*/5 * * * * docker system prune -f &>> /tmp/prune.log" >> fetch_updates')
sudo(f'echo "* * * * * sh {home_dir}/fetch_models.sh" >> fetch_updates')
sudo("crontab fetch_updates")
sudo("rm fetch_updates")
sudo("chmod -R a+w /tmp  ")

sudo(f"chmod a+w {home_dir}/fetch_models.sh")

with open(f"{home_dir}/fetch_models.sh", "r") as f:
    fetch_models = f.read().replace("python3 fetch_images.py", f"python3 {home_dir}/fetch_images.py")\
            .replace("fetch_images.py | sh", "fetch_images.py")\
            .replace("curl -o fetch_images.py", f"curl -o {home_dir}/fetch_images.py")
import time
time.sleep(3)
with open(f"{home_dir}/fetch_models.sh", "w") as f:
    f.write(fetch_models)

sudo("echo 2 >> /tmp/log")
update_pollinator = f"""#!/bin/bash
if [[ $(< /tmp/ipfs/output/done) == "true" ]]; then
    aws ecr get-login-password \\
        --region us-east-1 \\
    | docker login \\
        --username AWS \\
        --password-stdin 614871946825.dkr.ecr.us-east-1.amazonaws.com
    docker pull 614871946825.dkr.ecr.us-east-1.amazonaws.com/pollinations/pollinator:{dev_or_main} \\
        | grep "Status: Downloaded newer image" \\
        && (docker kill pollinator && sleep 3 || echo Pollinator not running...)
fi
docker run {gpu_flag} -d --rm \\
        --network host \\
        --name pollinator \\
        --env-file {home_dir}/.env \\
        -v /var/run/docker.sock:/var/run/docker.sock \\
        -v "$HOME/.aws/:/root/.aws/" \\
        --mount type=bind,source=/tmp/ipfs,target=/tmp/ipfs \\
        614871946825.dkr.ecr.us-east-1.amazonaws.com/pollinations/pollinator:{dev_or_main}
"""
with open(f"{home_dir}/pull_updates_and_restart.sh", "w") as f:
    f.writelines(update_pollinator)

sudo("curl -o images.json https://raw.githubusercontent.com/pollinations/model-index/main/images.json")
with open("images.json", "r") as f:
    images = json.load(f)

os.system("curl -o metadata.json https://raw.githubusercontent.com/pollinations/model-index/main/metadata.json")
with open("metadata.json", "r") as f:
    metadata = json.load(f)


pollinator_group = "T4"
with open(f"{home_dir}/.env", "r") as f:
    for line in f.readlines():
        env, val = line.split("=")
        if env == "POLLINATOR_GROUP":
            pollinator_group = val.strip()

log(f"# Pollinator group: {pollinator_group}")  


pull = """
aws ecr get-login-password \
    --region us-east-1 \
| docker login \
    --username AWS \
    --password-stdin 614871946825.dkr.ecr.us-east-1.amazonaws.com
docker pull {}
""".format

if not "docker pull" in os.popen("ps -ax").read():
    for _, image in images.items():
        try:
            assert pollinator_group in metadata[image.split("@")[0]]["meta"]["pollinator_group"]
        except (AssertionError, KeyError):
            log(f"# Ignore {image}")
            continue
        system(pull(image))
        if "@" in image:
            sudo(f"docker tag {image} {image.split('@')[0]}")
