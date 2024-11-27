import os
import json
import shutil
import time

import printer
import chunk_manager
import metadata_manager
import discord_manager
import github_manager

terminal_size = os.get_terminal_size()
terminal_width = terminal_size.columns
base_indent = 0

base_indent = 0

START_UPLOAD_FROM_CHUNK_ID = 0
TOTAL_CHUNKS = 0

def welcome_msg():

    global terminal_width

    text_color = "BRIGHT_YELLOW"
    text = " FILE UPLOAD WIZARD "
    dash = "-" * terminal_width
    space_before = (terminal_width - len(text))//2
    space_after = (terminal_width - space_before - len(text))
    text = "○" * space_before + text + "○" * space_after

    printer._print()
    printer._print(text, text_color, indent=base_indent)
    printer._print()
    printer._print()


def err_exit():
    printer._print(" ERR: INVALID INPUT ", color="RED", indent=base_indent)
    printer._print()
    exit()


def get_file_input_method():

    input_header_color = "CYAN"
    printer._print("Select your input method:", input_header_color, indent=base_indent+1)
    printer._print()

    option_color = "BRIGHT_WHITE"
    inp_list = ["[0] Enter file location in terminal", "[1] Open File Selector Dialog"]
    for inp in inp_list:
        printer._print(inp, option_color, indent=base_indent+2)
    printer._print()

    enter_choice_text = "Enter your choice (0 or 1): "
    enter_choice_color = "BRIGHT_YELLOW"
    printer._print(enter_choice_text, enter_choice_color, indent=base_indent+1, end='')

    choice = 0
    choice = input("")

    printer._print()

    try:
        choice = int(choice)
    except:
        err_exit()
    
    if choice < 0 or choice > 1:
        err_exit()
    
    return choice


def get_file_id():
    pass


def get_input_file_location(input_method):
    '''
    0 = Enter File location interminal
    1 = open tkinter dialog
    '''
    file_location = ""
    if input_method == 0:
        enter_location_color = "MAGENTA"
        printer._print("Enter File Location: ", enter_location_color, indent=base_indent+1, end='')
        file_location = input("")
    else:
        try:
            import tkinter as tk
            from tkinter import filedialog

            file_location = filedialog.askopenfilename()

        except:
            pass
    
    file_location = str(file_location)
    printer._print()
    printer._print()

    return file_location


def get_uploaded_ids():

    return metadata_manager.get_uploaded_ids()
    UPLOADED_CHUNK_LOC = "upload_metadata/uploaded_list.json"
    data = {}
    with open(UPLOADED_CHUNK_LOC, "r") as file:
        data = json.load(file)
    
    return data


def get_random_file_id(file_name):

    I = 0
    chunk_id = 0
    for x in file_name:
        if I > 20:
            break
        chunk_id = chunk_id*5 + ord(x)
        I+=1

    return str(chunk_id)


def get_last_updated_chunk_id(file_id):
    temp = {}
    print(f"upload_metadata/{file_id}.json")
    with open(f"upload_metadata/{file_id}.json", "r") as file:
        temp = json.load(file)
        pass
    temp = temp["chunk_metadata"]
    return len(temp)


def verify_file_id(random_id):
    uploaded_ids = get_uploaded_ids()

    if random_id in uploaded_ids:
        printer._print(f"Found {str(random_id)} is already present, do you want to continue upload from where you left off?(Y?N):", color="YELLOW", indent=base_indent+1, end='')
        opt = input()
        if opt == "Y" or opt == "y":
            return random_id
    
    while random_id in uploaded_ids:
        random_id += "_1"

    return random_id


def delete_chunk_storage_location(file_id):
    location = f"chunked_files/{file_id}"
    printer._print()
    printer._print("DELETING THE CHUNKED FILES", "RED", indent=base_indent)
    #print(os.path.abspath(location))
    print(location)
    shutil.rmtree(location)
    pass


def start_upload(file_id, FILE_CHUNK_PATH_LIST):
    global START_UPLOAD_FROM_CHUNK_ID
    global TOTAL_CHUNKS

    discord_manager.upload(file_id, FILE_CHUNK_PATH_LIST, START_UPLOAD_FROM_CHUNK_ID)


def init():
    global TOTAL_CHUNKS
    global START_UPLOAD_FROM_CHUNK_ID

    os.system("clear")
    welcome_msg()

    discord_manager.init("UPLOAD")

    input_method = get_file_input_method()

    file_location = get_input_file_location(input_method)

    file_name = os.path.basename(file_location)

    random_id = get_random_file_id(file_name)

    file_id = verify_file_id(random_id)

    chunk_manager.init()
    chunk_manager.create_chunk_dir(file_id)
    chunk_manager.generate_file_chunks(file_location, file_id)

    FILE_CHUNK_PATH_LIST = chunk_manager.get_chunk_list(file_id)

    FILE_CRED = f"-FILE LOC = {file_location} \n-FILE_ID = {file_id}\n-FILE_NAME = {file_name}\n-TOTAL CHUNKS = {len(FILE_CHUNK_PATH_LIST)}"
    printer._print(FILE_CRED, color="YELLOW")

    TOTAL_CHUNKS = len(FILE_CHUNK_PATH_LIST)

    START_UPLOAD_FROM_CHUNK_ID = metadata_manager.get_uploaded_chunks_count(file_id)

    if START_UPLOAD_FROM_CHUNK_ID == 0:
        metadata_manager.init()
        metadata_manager.create_metadata(file_id, file_name, discord_manager.channel_id,len(FILE_CHUNK_PATH_LIST))

    start_upload(file_id, FILE_CHUNK_PATH_LIST)
    delete_chunk_storage_location(file_id)
    github_manager.init("save")