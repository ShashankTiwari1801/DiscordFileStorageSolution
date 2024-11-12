import json
import printer


CHUNK_LIST_PATH = "upload_metadata/chunk_list.json"

base_indent = 4
def init():

    option_map = {}

    with open(CHUNK_LIST_PATH) as file:
        option_map = json.load(file)

    print("\n\n")
    I = 0
    res = {}
    printer._print("UPLOADED THE FOLLOWING FILES TO CLAD: \n", "YELLOW", indent=base_indent)
    for file_id in option_map:
        printer._print(f"[{I}]: {option_map[file_id]}", "GREEN", indent=base_indent+1)
        res[I] = f"upload_metadata/{file_id}.json"
        I+=1
    print("\n")
    return res
