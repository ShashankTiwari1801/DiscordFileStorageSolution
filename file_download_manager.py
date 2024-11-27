import os
import shutil

import printer
import uploaded_file_viewer
import chunk_manager
import discord_manager
import metadata_manager


terminal_size = os.get_terminal_size()
terminal_width = terminal_size.columns
base_indent = 0

base_indent = 0

def welcome_msg():

    global terminal_width

    text_color = "BRIGHT_BLUE"
    text = " FILE DOWNLOAD WIZARD "
    dash = "-" * terminal_width
    space_before = (terminal_width - len(text))//2
    space_after = (terminal_width - space_before - len(text))
    text = "●" * space_before + text + "●" * space_after

    printer._print()
    printer._print(text, text_color, indent=base_indent)
    printer._print()
    printer._print()


def err_exit():
    printer._print(" ERR: INVALID INPUT ", color="RED", indent=base_indent)
    printer._print()
    exit()


def get_input():
    get_input_color = "BRIGHT_BLUE"
    MSG = "ENTER THE ID OF FILE YOU WANT TO DOWNLOAD: "
    printer._print(MSG, color=get_input_color, indent=base_indent+2,end='')
    selected_id = input("")
    try:
        selected_id = int(selected_id)
    except:
        err_exit()
    return selected_id


def get_selected_file(file_list, selected_id):
    if selected_id >= len(file_list):
        err_exit()
    
    return file_list[selected_id]


def delete_chunk_storage_location(file_id):
    location = f"chunked_files/{file_id}"
    printer._print("DELETING THE CHUNKED FILES", "RED", indent=base_indent)
    #print(os.path.abspath(location))
    print(location)
    shutil.rmtree(location)
    pass


def init():
    os.system("clear")
    welcome_msg()

    discord_manager.init("DOWNLOAD")

    file_list = uploaded_file_viewer.init()
    selected_id = get_input()

    metadata_path = get_selected_file(file_list, selected_id)

    chunk_manager.init()

    file_id = metadata_manager.get_file_id(metadata_path)
    
    chunk_manager.create_chunk_dir(file_id)

    metadata = metadata_manager.load_metadata(file_id)

    UPLOADED_CHUNK_COUNT = len(chunk_manager.get_chunk_list(file_id))
    UPLOADED_CHUNK_COUNT = max(UPLOADED_CHUNK_COUNT-1, 0)

    discord_manager.download(file_id, metadata, UPLOADED_CHUNK_COUNT)

    UPLOADED_CHUNK_COUNT = len(chunk_manager.get_chunk_list(file_id))

    og_file_name = metadata["original_file_name"]
    total_chunks = metadata["total_chunks"]

    if UPLOADED_CHUNK_COUNT == total_chunks:
        printer._print()
        printer._print("DOWNLOADED ALL CHUNKS ...", "GREEN", indent=base_indent+1)
        chunk_manager.compile_chunks(file_id, og_file_name)
        delete_chunk_storage_location(file_id)
        pass