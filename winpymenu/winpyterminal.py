import os

CURSOR_UP_ONE = '\x1b[1A'
ERASE_LINE = '\x1b[2K'

def print_lines(lines:list[str])->int:
    count:int = 0
    for line in lines:
        print(line)
        count += (len(line) // int(os.get_terminal_size().columns)) + 1
    return count



def delete_lines(lines:int):
    """ Delete a number of lines from stodut

    Args:
        lines (int): Number of lines to be deleted
    """
    for i in range(lines):
        print(f"{CURSOR_UP_ONE}{ERASE_LINE}", end="")
