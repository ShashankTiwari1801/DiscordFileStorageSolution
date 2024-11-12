import printer
import json
import os

'''
SAMPLE METADATA:
abcd_metadata =
{
    "original_file_name": "abcd.txt",
    "channel_id": 100,
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
fin_map = {}

def save_json(file_id):
    global fin_map

    save_file_name = f"upload_metadata/{file_id}.json"

    with open(save_file_name, "w") as file:
        json.dump(fin_map , file)


def load_json(file_id):
    FILE_PATH = f"upload_metadata/{file_id}.json"
    metadata = {}
    with open(FILE_PATH, "r") as file:
        metadata = json.load(file)
    
    return metadata

def add_chunk_data(file_id,chunk_index, chunk_file_name, message_url, mesage_id):
    global fin_map

    fin_map = load_json(file_id)

    chunk_metadata = fin_map["chunk_metadata"]

    chunk_metadata[chunk_index] = {}
    chunk_metadata[chunk_index]["og_name"] = chunk_file_name
    chunk_metadata[chunk_index]["url"] = message_url
    chunk_metadata[chunk_index]["message_id"] = mesage_id

    save_json(file_id)
    pass

    
def init(og_file_name, total_chunks, channel_id, file_id):

    global fin_map

    fin_map["original_file_name"] = og_file_name
    fin_map["channel_id"] = channel_id
    fin_map["chunk_metadata"] = {}
    fin_map["total_chunks"] = total_chunks

    save_json(file_id)
    
'''
    chunk_list.sort()
    I = 0;
    for chunk_name in chunk_list:
        temp = {}
        temp["og_name"] = chunk_name
        temp["url"] = metadata_map[chunk_name]["url"]
        temp["message_id"] = metadata_map[chunk_name]["message_id"]
        #printer._print(f"{I} === {temp}", "YELLOW")
        fin_map["chunk_metadata"][I] = temp
        I+=1
''' 
    