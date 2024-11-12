'''
////// TODO:
make this work with both terminal and flask
'''

##################################################################################################################################
#                                                         WRITE CODE BELOW                                                       #
##################################################################################################################################

'''
import file_download_manager

import view_uploaded_file_list
'''

import file_upload_manager
import view_upload_file_list
import file_download_manager
import printer


choice_head = "Enter you choice(1, 2 or 3)"
choice_text = [
"[1] UPLOAD A FILE TO DISCORD",
"[2] DOWNLOAD FILE FROM DISCORD",
"[3] GET LIST OF UPLOADED FILES AND THEIR CHUNK ID",
"[4] EXIT"
]

while True:

    print("\n\n")
    printer._print(choice_head,"CYAN", end='\n\n',indent=1)
    for x in choice_text:
        printer._print(x,"BLUE", indent=2)
    print("\n\n")

    choice = input("Enter your choice: ")

    try:
        choice = (int)(choice)
    except:
        printer._print("\n\nInvalid Input...", "RED", end="\n\n")
        break

    if(choice < 1 or choice > 3):
        printer._print("\n\nClosing...", "RED", end="\n\n")
        break

    if(choice == 1):
        file_upload_manager.init()

    if choice == 2:
        file_download_manager.init()

    if(choice == 3):
        view_upload_file_list.init()
    
    break


#print(choice_text)