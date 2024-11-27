import os
import shutil
import json
import time

GITHUB_LINK = "https://github.com/ShashankTiwari1801/UPLOAD_METADATA_PRI.git"
METADATA_PATH = "security/GITHUB_DATA.json"
TEMP_DIR_NAME = "temp"
COPY_COMMAND = f"cp -r upload_metadata/ {TEMP_DIR_NAME}/"


def load_upload_status():
    data = {}
    with open(METADATA_PATH, "r") as file:
        data = json.load(file)
    #print(type(data["uploaded"]))
    return data


def downlaod_metadata():
    data = load_upload_status()
    is_upload_updated = data["uploaded"]
    cmd_list = [
        f"git clone {GITHUB_LINK} {TEMP_DIR_NAME}/",
        f"cp -r {TEMP_DIR_NAME}/*.json upload_metadata/"
    ]
    for cmd in cmd_list:
        os.system(cmd)
        time.sleep(5)

    pass


def update_GITHUB_metadata(updated_successfully):
    data = load_upload_status()
    data["uploaded"] = updated_successfully

    with open(METADATA_PATH, "w") as file:
        json.dump(data, file)


def upload_metadata():
    cmd_list = [
        f"git clone {GITHUB_LINK} {TEMP_DIR_NAME}/",
        f"cp -r upload_metadata/*.json {TEMP_DIR_NAME}/",
        f"git -C {TEMP_DIR_NAME} add .",
        f"git -C {TEMP_DIR_NAME} add .",
        f"git -C {TEMP_DIR_NAME} commit -m 'temp'",
        f"git -C {TEMP_DIR_NAME} push"
    ]

    for cmd in cmd_list:
        #print(f"      {cmd}:")
        os.system(cmd)
        time.sleep(5)
    
    update_GITHUB_metadata(True)

def make_directory():
    os.makedirs(f"{TEMP_DIR_NAME}", exist_ok=True)


def delete_temp():
    location = f"{TEMP_DIR_NAME}/"
    #print(os.path.abspath(location))
    #print(location)
    shutil.rmtree(location)


def copy_metadata():
    os.system(COPY_COMMAND)
    pass


def init(action_type):
    make_directory()
    if action_type == "load":
        downlaod_metadata()
        pass
    elif action_type == "save":
        upload_metadata()
        pass
    delete_temp()