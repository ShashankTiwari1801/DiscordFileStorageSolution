import os

import printer


def create_chunk_dir(file_id):
    os.makedirs(f"chunked_files/{file_id}", exist_ok=True)
    return f"chunked_files/{file_id}", file_id


def generate_file_chunks(file_path, file_id):
    cmd = f"split -b 5M -a 4 {file_path} chunked_files/{file_id}/{file_id}_part_"
    os.system(cmd)


def get_chunk_list(file_id):
    DIR_LOC = f"chunked_files/{file_id}/"
    files = [file for file in os.listdir(DIR_LOC) if os.path.isfile(os.path.join(DIR_LOC, file))]

    RES = []
    for file in files:
        RES.append(os.path.join(DIR_LOC, file))
    
    RES.sort()
    return RES


def compile_chunks(file_id, og_file_name):
    printer._print("COMPILING THE CHUNKS...", color="BLUE", indent=4)

    cmd = f"cat chunked_files/{file_id}/{file_id}_part_* > downloads/{og_file_name}"

    os.system(cmd)

    printer._print(f"CHUNKS DOWNLOADED AND COMPIPLED to {og_file_name} | file saved at downloads/{og_file_name}", color="GREEN", indent=4)
    print("\n")



def get_downloaded_chunks(file_id):
    DIR = f"chunked_files/{file_id}/"
    return os.listdir(DIR)

def init():
    pass