import os
import json

import printer
import loading_bar
import github_manager

base_indent = 1

MONTH_NAME = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]

def welcome_msg():
    MSG = "UPLOADED THE FOLLOWING TO THE CLAD!!: "
    printer._print(MSG, "BRIGHT_YELLOW", indent=base_indent)
    printer._print()
    pass


def list_files():
    directory_path = "upload_metadata/"
    files_with_paths = [os.path.join(directory_path, file) for file in os.listdir(directory_path) if file != "uploaded_list.json" and file != "chunk_list.json" and os.path.isfile(os.path.join(directory_path, file))]
    return files_with_paths


def get_file_name(metadata_path):
    data = {}
    with open(metadata_path , "r") as file:
        data = json.load(file)
    return data["original_file_name"]


def get_file_size(file_size_in_MB):
    '''
    1MB = 1MB
    10MB = 10MB
    100MB = 100MB
    1000MB = 1GB
    10000MB = 10GB
    100000MB = 100GB
    1000000MB = 1TB
    '''
    TB = file_size_in_MB // 1000000
    file_size_in_MB %= 1000000
    GB = file_size_in_MB // 1000
    file_size_in_MB %= 1000
    MB = file_size_in_MB
    res = ""
    if TB > 0:
        res += f"{TB}.{"{:03}".format(GB)}TB"
        pass
    elif GB > 0:
        res += f"{GB}.{"{:03}".format(MB)}GB"
        pass
    elif MB > 0:
        res += f"{MB}MB"

    return res


def get_total_chunks(metadata_path):
    data = {}
    with open(metadata_path , "r") as file:
        data = json.load(file)
    total_chunks = data["total_chunks"]
    file_size_in_MB = total_chunks * 5
    return get_file_size(file_size_in_MB)


def parse_timestamp(timestamp):
    timestamp = timestamp.split(" ")
    date_ = timestamp[0].split("-")
    time_ = timestamp[1].split(":")
    date_ = f"{date_[2]}{MONTH_NAME[int(date_[1])-1]}"
    time_ = ":".join(time_[:-1])
    return f"{date_}|{time_}"


def get_matrix(file_list):
    I = 0
    res = []
    HEADING = ["ID", "FILENAME", "CHUNK ID", "SIZE"]
    res.append(HEADING)
    for file_path in file_list:
        file_id = os.path.basename(file_path)[:-5]
        file_name = get_file_name(file_path)
        file_size = get_total_chunks(file_path)
        LINE = f"[{I}][{file_name}][{file_id}]"
        temp = []
        temp.append(str(I))
        temp.append(file_name)
        temp.append(file_id)
        temp.append(file_size)
        res.append(temp)
        I+=1

    return res


def parse_table(matrix):
    COLUMNS = []
    
    for i in range (0, len(matrix[0])):
        COLUMNS.append(0)
    
    for i in matrix:
        I = 0
        for _ in i:
            COLUMNS[I] = max(COLUMNS[I], len(_))
            I+=1
    
    for i in range(0, len(matrix)):
        for j in range(0, len(matrix[i])):
            matrix[i][j] = str(matrix[i][j]).center(COLUMNS[j])
    
    return matrix
    

def make_dark_backgound(text):
    return f"\033[48;5;{16}m{text}\033[0m"


def make_light_background(text):
    return f"\033[48;5;{237}m{text}\033[0m"


def print_files(file_list):

    matrix = get_matrix(file_list)
    matrix = parse_table(matrix)
    I = 0
    for _ in matrix:
        temp = ""
        for __ in _:
            temp += f"[{__}]"
            pass
        #printer._print(temp, color="BRIGHT_MAGENTA", indent=0)
        text = loading_bar.decorate(temp, I%20)
        # if I % 2 == 1:
        #     text = make_dark_backgound(text)
        # else:
        #     text = make_light_background(text)
        print(text)
        I+=1


def init():
    welcome_msg()
    #github_manager.init("load")
    file_list = list_files()
    print_files(file_list)
    printer._print()
    printer._print()
    return file_list
