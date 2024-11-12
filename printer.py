COLOR_MAP = {
    "RED": "\033[31m",
    "GREEN": "\033[32m",
    "BLUE": "\033[34m",
    "YELLOW": "\033[33m",
    "MAGENTA": "\033[35m",
    "CYAN": "\033[36m",
    "WHITE": "\033[37m",
    "BLACK": "\033[30m",
    "BRIGHT_RED": "\033[91m",
    "BRIGHT_GREEN": "\033[92m",
    "BRIGHT_YELLOW": "\033[93m",
    "BRIGHT_BLUE": "\033[94m",
    "BRIGHT_MAGENTA": "\033[95m",
    "BRIGHT_CYAN": "\033[96m",
    "BRIGHT_WHITE": "\033[97m",
    "GRAY": "\033[90m",
    "END": "\033[0m"
}


def get_indent(depth):
    res = "     "
    res *= depth
    return res

def get_lines_after(lines):
    res = "\n"
    res *= lines
    return res

def _print(text, color, end = '\n', indent = 0):
    txt = f"{get_indent(indent)}{COLOR_MAP[color]}{text}{COLOR_MAP['END']}"
    print(txt, end=end)