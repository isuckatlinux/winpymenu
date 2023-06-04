import os
import sys

CURSOR_UP_ONE = '\x1b[1A'
ERASE_LINE = '\x1b[2K'

CURSOR_BACKWARD = '\x1b[D'

GET_CURSOR_POSITION = '\x1b[6n'



def print_lines(lines:list[str], searching_buffer:str)->int:
    count:int = 0
    for line in lines:
        print(line)
        count += (len(line) // int(os.get_terminal_size().columns)) + 1

    for i in range(count+1, os.get_terminal_size().lines):
        print()
    
    print(searching_buffer, end="", flush=True)

    return count

def delete_lines(lines:int):
    """ Delete a number of lines from stodut

    Args:
        lines (int): Number of lines to be deleted
    """
    for i in range(lines):
        print(f"{CURSOR_UP_ONE}{ERASE_LINE}", end="")

def delete_all_lines(searching_buffer:str, lines:int):
    print(CURSOR_BACKWARD*len(searching_buffer), end="")

    for index in range(0, lines+1):
        print(f"{ERASE_LINE}", end="")
        if index != lines:
            print(f"{CURSOR_UP_ONE}", end="")


def cursor_backwards(times:int=1):
    print(CURSOR_BACKWARD*times, end="")


def is_decodable(byte:bytes, encoding='utf-8'):
    try:
        byte.decode(encoding)
        return True
    except UnicodeDecodeError:
        return False