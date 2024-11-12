import os
import printer
import view_upload_file_list
import json
import discord
import shutil
import file_compiler
import loading_bar

discord_token = ""
channel_id = ""

chunk_id = ""

metadata_map = {}

intents = discord.Intents.default()
client = discord.Client(intents=intents)

base_indent = 2

####################################### DISCORD API ############################################

async def download_attachment(message_id, save_dir_path, file_name):

    global channel_id

    channel = client.get_channel(channel_id)

    message = await channel.fetch_message(message_id)

    attachment = message.attachments[0]

    save_file_path = f"{save_dir_path}/{file_name}"

    await attachment.save(save_file_path)
    #printer._print(f"Saved file @ file_save_path : {save_file_path}", color="GREEN", indent=5)

    pass

@client.event
async def on_ready():

    global chunk_id
    global metadata_map

    print()
    printer._print(f'Logged in as {client.user}', color="WHITE", indent=base_indent+2)
    print()
    
    total_chunks = int(metadata_map["total_chunks"])

    chunk_metadata = metadata_map["chunk_metadata"]

    save_dir_path = f"chunked_files/{chunk_id}"

    printer._print(save_dir_path, color="MAGENTA", indent=base_indent+2)

    for i in range(0,total_chunks):
        og_name = chunk_metadata[str(i)]["og_name"]
        message_id = chunk_metadata[str(i)]["message_id"]
        printer._print(loading_bar.print_loading_msg(i+1, total_chunks, "Download", indent=5), color="MAGENTA", end='', indent=2)
        await download_attachment(message_id, save_dir_path,og_name)
        pass
    print("\n")
    #printer._print(metadata_map, color="YELLOW", indent=3)

    await client.close()

####################################### /DISCORD API ###########################################


def welcome_message():

    print("\n\n")

    msg = "FILE DOWNLOADER WIZARD"
    temp = "+" + ("="*len(msg)*3) + "+"
    printer._print(temp, "YELLOW", indent=base_indent)


    temp = "|" + (" "*len(msg)) + msg + (" "*len(msg)) + "|"
    printer._print(temp, "YELLOW", indent=base_indent)


    temp = "+" + ("="*len(msg)*3) + "+"
    printer._print(temp, "YELLOW", indent=base_indent)
    pass

def take_input():
    printer._print("ENTER THE ID OF THE FILE YOU WANT TO DOWNLOAD", color="YELLOW", indent=base_indent+1, end=': ')
    chunk_id = input()
    print("\n")
    return chunk_id

def print_confirmation_msg(chunk_id, metadata_location):
    printer._print(f"found {chunk_id}. Found metadata @{metadata_location}, Downloading File...", color="BLUE", indent=base_indent+1)
    print()
    pass

def fetch_matadata(file_location):

    data = {}

    with open(file_location, "r") as file:
        data = json.load(file)
    
    return data

def generate_chunk_id(file_path):
    global uploading_file_name

    file_name = os.path.basename(file_path)
    uploading_file_name = file_name
    file_name = file_name.split(".")[0]
    return file_name

def setup_download_location(chunk_id):
    os.makedirs(f"chunked_files/{chunk_id}", exist_ok=True)
    pass

def download_chunks():
    pass

def get_api_credentials():
    data = {}
    with open("security/API_DATA.json") as file:
        data = json.load(file)
    return data

def delete_chunks(chunk_id):
    location = f"chunked_files/{chunk_id}"
    #print(os.path.abspath(location))
    #print(location)
    shutil.rmtree(location)

def init():

    global discord_token
    global channel_id
    global metadata_map
    global chunk_id

    api_cred = get_api_credentials()

    discord_token = api_cred["APP_TOKEN"]
    channel_id = api_cred["CHANNEL_IDS"]["UPLOAD"]

    welcome_message()
    uploaded_file_dict = view_upload_file_list.init()
    
    download_id = int(take_input())

    if download_id not in uploaded_file_dict.keys():
        printer._print(f"Entered ID \"[{download_id}]\" doesn't exist", color="RED", indent=base_indent+1)
        print("\n")
        exit()
    
    metadata_file_path = uploaded_file_dict[download_id] # File Location of metadata.json of the file

    print_confirmation_msg(download_id, metadata_file_path)

    chunk_id = generate_chunk_id(metadata_file_path)

    setup_download_location(chunk_id)

    metadata_map = fetch_matadata(metadata_file_path)

    client.run(discord_token)

    save_dir_path = f"chunked_files/{chunk_id}"

    og_file_name = metadata_map["original_file_name"]

    file_compiler.init(save_dir_path, og_file_name, chunk_id)

    delete_chunks(chunk_id)
    print()
