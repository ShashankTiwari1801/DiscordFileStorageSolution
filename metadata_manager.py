import printer
import uploaded_file_viewer

import time
import json
import os
from datetime import datetime

'''
METADATA STRUCTURE

SAMPLE METADATA:
abcd_metadata =
{
    "original_file_name": "abcd.txt",
    "channel_id": 100,
    "timestamp": "",
    "file_id": "",
    "total_chunks": 10,
    "chunk_metadata": {
        "0": {
            "og_name": "testBook_part_aa",
            "url": "abcd.xyz",
            "message_id": 1234
        }
    }
}

'''


def get_uploaded_ids():

    files = uploaded_file_viewer.list_files()
    id_list = []
    for file_name in files:
        temp_name = os.path.basename(file_name)
        temp_name = temp_name[:-5]
        id_list.append(temp_name)
    
    return id_list

    UPLOADED_CHUNK_LOC = "upload_metadata/uploaded_list.json"
    data = {}
    with open(UPLOADED_CHUNK_LOC, "r") as file:
        data = json.load(file)
    
    return data


def get_uploaded_chunks_count(file_id):

    if file_id in get_uploaded_ids():
        metadata = load_metadata(file_id)
        chunk_list = metadata["chunk_metadata"]
        uploaded_chunks = len(chunk_list)
        last_id = uploaded_chunks - 1
        return max(0, last_id)
    
    return 0


def get_file_path(file_id):
    FILE_NAME = f"{file_id}.json"
    FILE_LOC = f"upload_metadata/{FILE_NAME}"
    return FILE_LOC


def get_file_id(metadata_file_path):
    temp = os.path.basename(metadata_file_path)
    return temp[:-5]
    pass


def get_timestamp():
    return str(datetime.now())
    pass


def load_metadata(file_id):
    FILE_LOC = get_file_path(file_id)
    data = {}
    with open(FILE_LOC, "r") as file:
        data = json.load(file)
    
    return data


def save_metadata_in_list(file_id, og_file_name):
    data = {}
    LIST_PATH = "upload_metadata/uploaded_list.json"
    with open(LIST_PATH, "r") as file:
        data = json.load(file)
        pass
    
    data[file_id] = og_file_name

    with open(LIST_PATH, "w") as file:
        json.dump(data, file)


def add_chunk_detail_in_metadata(file_id, chunk_id, chunk_name, url, message_id):
    chunk_data = {}
    chunk_data["og_name"] = chunk_name
    # chunk_data["url"] = url
    chunk_data["message_id"] = message_id

    metadata = load_metadata(file_id)
    chunk_metadata = metadata["chunk_metadata"]
    chunk_metadata[str(chunk_id)] = chunk_data

    FILE_LOC = get_file_path(file_id)

    with open(FILE_LOC, "w") as file:
        json.dump(metadata, file)


def create_metadata(file_id, og_file_name, channel_id, total_chunks):
    metadata = {}
    FILE_NAME = f"{file_id}.json"
    FILE_LOC = f"upload_metadata/{FILE_NAME}"
    metadata["original_file_name"] = og_file_name
    metadata["channel_id"] = channel_id
    metadata["file_id"] = file_id
    metadata["timestamp"] = get_timestamp()
    metadata["total_chunks"] = total_chunks
    metadata["chunk_metadata"] = {}

    with open(FILE_LOC, "w") as file:
        json.dump(metadata, file)

    #save_metadata_in_list(file_id, og_file_name)

def init():
    print(datetime.now())
    pass
