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

gpu_flag = "--gpus all" if os.system("nvidia-smi") == 0 else ""

with open(f"{home_dir}/pull_updates_and_restart.sh", "r") as f:
    content = f.read()
    dev_or_main = "dev" if "pollinator:dev" in content else "main"

def system(cmd):
    os.system(f"sudo {cmd}")

system("crontab -r")
system("crontab -l > fetch_updates")
system('echo "*/5 * * * * /bin/bash /home/nielswarncke/pull_updates_and_restart.sh &>> /tmp/pollinator.log" >> fetch_updates')
system('echo "*/5 * * * * docker system prune -f &>> /tmp/prune.log" >> fetch_updates')
system('echo "*/5 * * * * ps -ax | grep fetch_models | wc -l | grep 1 && sh /home/nielswarncke/fetch_models.sh &>> /tmp/fetch.log" >> fetch_updates')
system("crontab fetch_updates")
system("rm fetch_updates")


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
    docker run {gpu_flag} -d --rm \\
            --network host \\
            --name pollinator \\
            --env-file {home_dir}/.env \\
            -v /var/run/docker.sock:/var/run/docker.sock \\
            -v "$HOME/.aws/:/root/.aws/" \\
            --mount type=bind,source=/tmp/ipfs,target=/tmp/ipfs \\
            614871946825.dkr.ecr.us-east-1.amazonaws.com/pollinations/pollinator:{dev_or_main}
fi
"""
with open(f"{home_dir}/pull_updates_and_restart.sh", "w") as f:
    f.writelines(update_pollinator)

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


