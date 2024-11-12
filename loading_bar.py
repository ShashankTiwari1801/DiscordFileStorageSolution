import time

'''

[Uploaded 25/100 files] - Uploading "document_26.txt" (26% complete)


'''
icon_map = {
    "full" : "█",
    "half" : "▓",
    "none" : "▒"
}
'''

    "full" : "⠿",
    "half" : "⠇",
    "none" : "⠀"

┃▒▒▒▓▓▓██████           ┃
'''
def get_indent(depth):
    res = f"[{icon_map["full"]}{icon_map["full"]}{icon_map["half"]}{icon_map["none"]}{icon_map["none"]}]"
    res *= depth
    return res

def get_progress_bar(progress):
    '''
    20 bars = 100%
    1 bar = 5%
    1/2 bar = [2.5% - 5%)
    '''
    full_bars = int(progress//5)
    full_bars = icon_map["full"] * full_bars

    partial_bars = ""
    partial_val = progress - (progress//5)

    if partial_val > 3:
        partial_bars = icon_map["half"]

    rem = 20 - len(partial_bars) - len(full_bars)

    rem = icon_map["none"]*rem

    res = f"┃{full_bars}{partial_bars}{rem}┃"

    return res


def print_loading_msg(current_progress, max_value,transfer_type, indent = 0):

    progress = current_progress/max_value
    progress *= 100

    progress = int(progress*100) / 100

    indent = get_indent(indent)

    indent = get_progress_bar(progress)

    text = f"\r{indent}[{transfer_type}ed {current_progress}/{max_value} files] - {transfer_type}ing ({progress}% completed)"

    return text
    #print(f"\r{text}", end='')
