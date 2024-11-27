import os

import printer

terminal_size = os.get_terminal_size()
terminal_width = terminal_size.columns

bars = [' ', '▁', '▂', '▃', '▃', '▄', '▄', '▅', '▆', '▇', '█']

bars = [' ', '▁', '▂', '▃', '▄', '█']


def decorate(text, index):
    colors = [
        201, 200, 199,   # Violet
        54, 55,           # Indigo
        18, 19, 20,       # Blue
        46, 47, 48, 49,   # Green
        226, 227, 228,    # Yellow
        220, 214,         # Orange
        196, 160, 124     # Red
    ]

    #print(f"\033[38;5;{colors[index]}m{text}\033[0m")
    return f"\033[38;5;{colors[index]}m{text}\033[0m"


def get_bars(percent):
    og = percent
    empty = 100-percent
    empty = " "*int(empty/5)
    res = ""
    
    while percent >= 5:
        percent -= 5
        res += bars[-1]


    # while percent >= 10:
    #     percent -= 10
    #     res += bars[-1]
    
    if percent > 0:
        res += bars[percent]

    # 97% => 0 9 7

    hun = og // 100;
    ten = (og % 100) // 10;
    one = og % 10;

    res += empty

    temp = list(res)
    temp[8] = str(hun)
    temp[9] = str(ten)
    temp[10] = str(one)
    temp[11] = "%"

    for i in range(0, len(temp)):
        temp[i] = decorate(temp[i], i)
    res = "".join(temp)

    res = f"{res}"
    
    return res
    
'''
┃███████▃  ┃ = 74%



┃█38%███▃            ┃ = 38%
01234567890123456789012345

|█38%███▃            |
 01234567890123456789
012345678901
- - - - - - - -
▁ ▂ ▃ ▄ ▅ ▆ ▇ █

0  - ' '
1  - '▁'
2  - '▂'
3  - '▃'
4  - '▃'
5  - '▄'
6  - '▄'
7  - '▅'
8  - '▆'
9  - '▇'
10 - '█'


┃▒▒▒▓▓▓▓▓███████        ┃


'''
    
def get_loading_bar(current, total, TYPE):
    global terminal_width

    percent = (current / total) * 100

    PART1 = f"\r┃{get_bars(int(percent))}┃"
    PART2 = f"{current}/{total} Files {TYPE}loaded"

    PART1_LEN = 22

    if PART1_LEN + len(PART2) < terminal_width:
        PART1 += PART2
    
    print(PART1, end='')


# import time

# N = 100
# for i in range(0,N):
#     get_bars(i)
#     get_loading_bar(i+1, N, "Up", "temp_part_aaaa")
#     time.sleep(0.1)
