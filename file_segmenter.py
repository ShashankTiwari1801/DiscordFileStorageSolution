'''
CHUNKS WiLL BESTORED IN AND AS:

    chunked_ifles/<chunk_id>/<chunk_id>_part_aa

'''

import os
import printer
from pathlib import Path

base_indent = 3

def init_msg(file_name, chunk_id):
    print("\n")
    printer._print(f"SPLITTING [{file_name}] to smaller chunks ({chunk_id}_part_****)(1MB each)...", "BRIGHT_MAGENTA", indent=base_indent+2)


def get_file_name(file_path):
    file_name = os.path.basename(file_path)
    return file_name


def segment_file(file_path, chunk_id):
    os.makedirs(f"chunked_files/{chunk_id}", exist_ok=True)
    cmd = f"split -b 5M -a 4 {file_path} chunked_files/{chunk_id}/{chunk_id}_part_"
    os.system(cmd)

    printer._print(f"FILE SUCCESSFULLY SEGMENTED, SEGMENTED FRAGMENTS STORED in [chunked_files/{chunk_id}]", "GREEN", indent=base_indent+2)
    print("\n\n")
    pass

def get_chunk_list(chunk_id):
    path = f"chunked_files/{chunk_id}"
    path = Path(path)
    return [str(file) for file in path.rglob('*') if file.is_file()]
    
def parse_chunk_list(chunk_list):
    res = []

    for chunk in chunk_list:
        temp = chunk.split("/")[-1]
        res.append(temp)
    
    return res


def init(file_path, chunk_id):

    file_name = get_file_name(file_path)
    init_msg(file_name, chunk_id)
    segment_file(file_path, chunk_id)

    chunk_list = get_chunk_list(chunk_id)
    chunk_list.sort()
    return chunk_list, parse_chunk_list(chunk_list)