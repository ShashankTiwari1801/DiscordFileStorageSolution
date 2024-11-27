import os
import json
import time


import discord

import printer
import loading_bar
import metadata_manager

# Discord things

DISCORD_SECURITY_PATH = "security/API_DATA.json"
discord_token = ""
channel_name = "UPLOAD2"
channel_id = ""

intents = discord.Intents.default()
client = discord.Client(intents=intents)

FILE_ID = 0
CHUNK_PATHS = []
START_ID = 0
TOTAL_CHUNKS = 0

CHUNK_METADATA = {}

base_indent = 1

TRANSFER_TYPE = ""  # "UPLOAD" or "DOWNLOAD"
#****************

def load_discord_cred():

    global discord_token
    global channel_id
    global channel_name

    data = {}
    with open(DISCORD_SECURITY_PATH, "r") as file:
        data = json.load(file)

    discord_token = data["APP_TOKEN"]
    channel_id = data["CHANNEL_IDS"][channel_name]


async def upload_file(file_id, chunk_id, path_to_chunk):
    global client
    global channel_id

    channel = client.get_channel(channel_id)

    if channel is None:
        printer._print("INVALID CHANNEL","RED", indent = 3)
        return
    
    with open(path_to_chunk, "rb") as file:
        time.sleep(0.5)
        
        message = await channel.send(file=discord.File(file, os.path.basename(path_to_chunk)))

        attachment = message.attachments[0]
        msg_id = message.id
        file_url = attachment.url
        og_file_name = os.path.basename(path_to_chunk)

        metadata_manager.add_chunk_detail_in_metadata(file_id, chunk_id, og_file_name, file_url, msg_id)
        

async def download_file(message_id, save_dir_path, file_name):

    channel = client.get_channel(channel_id)

    message = await channel.fetch_message(message_id)

    attachment = message.attachments[0]

    save_file_path = f"{save_dir_path}/{file_name}"

    await attachment.save(save_file_path)



@client.event
async def on_ready():

    global START_ID
    global TRANSFER_TYPE
    global CHUNK_METADATA
    global FILE_ID

    printer._print(f"Logged in as {client.user}", color = "GREEN", indent = base_indent+2)
    printer._print()
    i = START_ID

    if TRANSFER_TYPE == "UPLOAD":
        while i < TOTAL_CHUNKS:

            loading_bar.get_loading_bar(i, TOTAL_CHUNKS, "Up")
            await upload_file(FILE_ID, i, CHUNK_PATHS[i])
            loading_bar.get_loading_bar(i+1, TOTAL_CHUNKS, "Up")
            i+=1
            pass

    elif TRANSFER_TYPE == "DOWNLOAD":

        while i < TOTAL_CHUNKS:
            chunk_id = f"{i}"
            chunk_name = CHUNK_METADATA[chunk_id]["og_name"]
            message_id = CHUNK_METADATA[chunk_id]["message_id"]
            save_dir_path = f"chunked_files/{FILE_ID}"

            loading_bar.get_loading_bar(i, TOTAL_CHUNKS, "Down")
            await download_file(message_id, save_dir_path, chunk_name)
            loading_bar.get_loading_bar(i+1, TOTAL_CHUNKS, "Down")
            i+=1
        pass

    await client.close()



def upload(file_id, FILE_CHUNK_PATH_LIST, START_UPLOAD_FROM_CHUNK_ID):
    global FILE_ID
    global CHUNK_PATHS
    global START_ID
    global TOTAL_CHUNKS

    FILE_ID = file_id
    CHUNK_PATHS = FILE_CHUNK_PATH_LIST
    START_ID = START_UPLOAD_FROM_CHUNK_ID
    TOTAL_CHUNKS = len(CHUNK_PATHS)

    client.run(discord_token)


def download(file_id, download_metadata, start_id):
    global FILE_ID
    global TOTAL_CHUNKS
    global START_ID
    global CHUNK_METADATA
    global channel_id

    FILE_ID = file_id
    TOTAL_CHUNKS = download_metadata["total_chunks"]
    START_ID = start_id
    CHUNK_METADATA = download_metadata["chunk_metadata"]
    channel_id = download_metadata["channel_id"]


    client.run(discord_token)
    pass

def init(tranfer_type):
    global TRANSFER_TYPE

    TRANSFER_TYPE = tranfer_type

    load_discord_cred()
    pass