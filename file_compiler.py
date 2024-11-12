'''
COMBINES THE CHUNKS BACK TO OG FILE
'''
import os
import printer

def init(chunks_path, og_file_name, chunk_id):

    printer._print("COMPILING THE CHUNKS...", color="BLUE", indent=4)
    print("")

    cmd = f"cat {chunks_path}/{chunk_id}_part_* > downloads/{og_file_name}"
    # printer._print(cmd, color="RED", indent= 7)
    os.system(cmd)

    printer._print(f"CHUNKS DOWNLOADED AND COMPIPLED to {og_file_name} | file saved at downloads/{og_file_name}", color="GREEN", indent=4)
    print("\n")
    pass