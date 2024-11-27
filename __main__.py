import printer
import os

import file_upload_manager
import file_download_manager
import uploaded_file_viewer
import github_manager


github_manager.init("load")

os.system("clear")

terminal_size = os.get_terminal_size()
terminal_width = terminal_size.columns
base_indent = 0

def welcome_msg():

    global terminal_width

    text_color = "BRIGHT_GREEN"
    text = " FILE STORAGE SOLUTION "
    dash = "-" * terminal_width
    space_before = (terminal_width - len(text))//2
    space_after = (terminal_width - space_before - len(text))
    text = " " * space_before + text

    printer._print()
    printer._print(dash, text_color, indent=base_indent)
    printer._print(text, text_color, indent=base_indent)
    printer._print(dash, text_color, indent=base_indent)

welcome_msg()

printer._print()
printer._print()

choice_head = "Select you choice(1, 2 or 3)"
choice_text = [
    "[1] UPLOAD A FILE TO SSTORAGE",
    "[2] DOWNLOAD FILE FROM SSTORAGE",
    "[3] GET LIST OF UPLOADED FILES AND THEIR CHUNK ID",
    "[4] EXIT"
]

head_color = "CYAN"
printer._print(choice_head, head_color, indent=base_indent+1)

printer._print()

choice_color = "BRIGHT_WHITE"
for choise in choice_text:
    printer._print(choise, choice_color, indent=base_indent+2)

printer._print()

enter_choice_text = "Enter your choice (1-4): "
enter_choice_color = "BRIGHT_YELLOW"
printer._print(enter_choice_text, enter_choice_color, indent=base_indent+1, end='')

choice = 0
choice = input("")

printer._print()

try:
    choice = int(choice)
except:
    printer._print(" ERR: INVALID INPUT ", color="RED", indent=base_indent)
    printer._print()
    exit()

printer._print()
printer._print()
printer._print()

if choice == 1:
    file_upload_manager.init()

elif choice == 2:
    file_download_manager.init()

elif choice == 3:
    uploaded_file_viewer.init()

elif choice == 4:
    exit()
