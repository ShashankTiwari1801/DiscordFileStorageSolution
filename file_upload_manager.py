'''
FIlE UPLOAD PIPELINE:
☐☑
    . ☑ WELCOME MESSAGE
    . ☑ Select File
    . ☑ Genertate File_ID
    . ☑ Create Chunk Storage location
    . ☑ Segment the files (Split into chunks) > Chunk Storage
    . ☑ Upload chunks to discord 
    . ☑ Delete chunks and chunks storage location
    . ☐ Save the Metadata

base indent depth = 2
'''
import os
import json

import printer
import file_segmenter
import update_metadata
import loading_bar

import discord
import tkinter as tk
from tkinter import filedialog
import shutil

# global chunk list containing all uploaded fies
CHUNK_LIST_FILE_PATH = "upload_metadata/chunk_list.json"

base_indent = 2
total_chunks = 0

chunked_file_loc_list = []
file_id = ""

START_UPLOAD_FROM_ID = 0
# Discord things

DISCORD_SECURITY_PATH = "security/API_DATA.json"
discord_token = ""
channel_id = ""

intents = discord.Intents.default()
client = discord.Client(intents=intents)

#****************

def welcome_message(color):
    print("\n\n")
    
    msg = "FILE UPLOADER WIZARD"
    temp = "+" + ("="*len(msg)*3) + "+"
    printer._print(temp, color, indent=base_indent)


    temp = "|" + (" "*len(msg)) + msg + (" "*len(msg)) + "|"
    printer._print(temp, color, indent=base_indent)


    temp = "+" + ("="*len(msg)*3) + "+"
    printer._print(temp, color, indent=base_indent)

    print("\n\n")


def file_selector_method():

    printer._print("Select your input method:\n", "WHITE", indent=base_indent+1)
    inp_list = ["enter file location in terminal", "open file selector dialog"]


    for i in range(0,2):
        printer._print(f"[{i}] {inp_list[i]}", color="BRIGHT_CYAN", indent=base_indent+2)

    try:
        res = int(input("\nEnter your choice: "))
        
        if res < 0 or res > 1:
            printer._print(f"INVALID INPUT\n", "BRIGHT_RED", indent=base_indent+1)
            return file_selector_method()
    except:
        printer._print(f"INVALUD INPUT\n", "BRIGHT_RED", indent=base_indent+1)
        return file_selector_method()
    
    return res


def file_selector():
    file_location = ""
    _file_selector_method = file_selector_method()

    if _file_selector_method == 0:
        printer._print("ENTER THE LOCATION OF THE FILE YOU WANT TO UPLOAD: ", color="YELLOW", indent=base_indent+1, end=': ')
        file_location = input("")
    else:
        file_location = filedialog.askopenfilename()

    return file_location


def verify_path(file_path):
    if os.path.exists(file_path):
        printer._print(f"FILE FOUND @ ({file_path})...", "GREEN", indent=base_indent+1)
        print("\n")
    else:
        printer._print(f"FILE NOT FOUND @ ({file_path})...", "RED", indent=base_indent+1)
        print("\n")
        exit()


def get_random_file_id(file_path):

    I = 0
    chunk_id = 0
    for x in file_path:
        if I > 20:
            break
        chunk_id = chunk_id*5 + ord(x)
        I+=1

    return chunk_id

def get_last_updated_chunk_id(file_id):
    temp = {}
    print(f"upload_metadata/{file_id}.json")
    with open(f"upload_metadata/{file_id}.json", "r") as file:
        temp = json.load(file)
        pass
    temp = temp["chunk_metadata"]
    return len(temp)

def get_file_id(file_name):

    global START_UPLOAD_FROM_ID

    file_id = ""

    file_id = get_random_file_id(file_name)
    
    uploaded_ids = get_file_id_list()

    if str(file_id) in uploaded_ids:
        printer._print(f"Found {str(file_id)} is already present, do you want to continue upload from where you left off?(Y?N): ", color="BLUE" , indent=base_indent+1, end='')
        opt = input()
        if opt == "Y" or opt == "y":
            #<SET START_UPLOAD_FROM_ID to last updated - 1>
            START_UPLOAD_FROM_ID = max(get_last_updated_chunk_id(file_id)-1, 0)
            print(START_UPLOAD_FROM_ID)
            return str(file_id)

    else:
        printer._print(f"Starting the file upload from the beginning ", color="BRIGHT_YELLOW", indent= base_indent+2)
        START_UPLOAD_FROM_ID = 0
        while str(file_id) in uploaded_ids:
            file_id = str(file_id) + "_1"
    
    
    uploaded_ids[file_id] = file_name
    save_file_id(uploaded_ids)
    return str(file_id)


def save_file_id(uploaded_ids):
    # updates the chunk_list.json file after adding 
    with open(CHUNK_LIST_FILE_PATH, "w") as file:
        json.dump(uploaded_ids , file)
    pass


def get_file_id_list():
    '''
    {
        "<chunk_id>":"file_name.ext"
    }
    '''
    temp = {}
    with open(CHUNK_LIST_FILE_PATH, "r") as file:
        temp = json.load(file)
    
    return temp


def delete_chunk_storage_location(file_id):
    location = f"chunked_files/{file_id}"
    printer._print("DELETING THE CHUNKED FILES", "RED", indent=base_indent)
    #print(os.path.abspath(location))
    #print(location)
    shutil.rmtree(location)
    pass


def load_discord_credentials():

    global DISCORD_SECURITY_PATH
    global discord_token
    global channel_id

    api_cred = {}

    with open(DISCORD_SECURITY_PATH) as file:
        api_cred = json.load(file)
    
    discord_token = api_cred["APP_TOKEN"]
    channel_id = api_cred["CHANNEL_IDS"]["UPLOAD"]


async def upload_and_save_file(path_to_chunk_file, ID):
    global channel_id
    global client
    global chunk_meta_data

    channel = client.get_channel(channel_id)

    if channel is not None:
        with open(path_to_chunk_file, "rb") as file:
            
            message = await channel.send(file=discord.File(file, os.path.basename(path_to_chunk_file)))
            
            attachment = message.attachments[0]
            msg_id = message.id
            file_url = attachment.url
            og_file_name = os.path.basename(path_to_chunk_file)

            update_metadata.add_chunk_data(file_id, ID, og_file_name, file_url, msg_id)

            #chunk_meta_data[og_file_name] = {}
            #chunk_meta_data[og_file_name]["message_id"] = msg_id
            #chunk_meta_data[og_file_name]["url"] = file_url
    pass


@client.event
async def on_ready():

    global START_UPLOAD_FROM_ID

    printer._print(f'Logged in as {client.user}', "GREEN", indent=base_indent+2)

    I = START_UPLOAD_FROM_ID

    while I < len(chunked_file_loc_list):
        #print(chunked_file_loc_list[I])
        printer._print(loading_bar.print_loading_msg(I+1, total_chunks, "Upload", indent=5), color="MAGENTA", end='', indent=2)
        await upload_and_save_file(chunked_file_loc_list[I], I)
        I+=1
        pass

    for chunk_path in chunked_file_loc_list:
        pass    
    
    print("\n")
    printer._print("UPLOAD COMPLETE", color="YELLOW", indent=4)
    #printer._print(str(chunk_meta_data), "RED", indent=6)
    await client.close()


def init():

    global total_chunks
    global channel_id
    global chunked_file_loc_list
    global file_id
    global START_UPLOAD_FROM_ID

    welcome_message("BRIGHT_YELLOW")
    file_location = file_selector()
    verify_path(file_location)
    
    file_name = os.path.basename(file_location)

    file_id = get_file_id(file_name)

    chunked_file_loc_list, chunk_name_list = file_segmenter.init(file_location, file_id)

    total_chunks = len(chunk_name_list)

    load_discord_credentials()

    if START_UPLOAD_FROM_ID == 0:
        print("CREATE NEW METADATA")
        #update_metadata.init(file_name, total_chunks, channel_id, file_id)

    client.run(discord_token)

    delete_chunk_storage_location(file_id)
