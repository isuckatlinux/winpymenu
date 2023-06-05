import os
from sys import platform

CURSOR_UP_ONE = '\x1b[1A'
ERASE_LINE = '\x1b[2K'

CURSOR_BACKWARD = '\x1b[D'

GET_CURSOR_POSITION = '\x1b[6n'

def print_lines(lines:list[str], searching_buffer:str):
    """ Print lines to the stdout

    Args:
        lines (list[str]): list of strings to be printed
        searching_buffer (str): to print the searching buffer
    """
    count:int = 0

    for line in lines:
        print(line)
        count += (len(line) // int(os.get_terminal_size().columns)) + 1 # Variable to store all the terminal lines used to print

    # Print void lines starting from the last used line of the terminal.
    for i in range(count+1, os.get_terminal_size().lines):
        print()
    
    # Prints the searching buffer.
    print(searching_buffer, end="", flush=True)

def delete_lines(lines:int):
    """ Delete a number of lines from stodut

    Args:
        lines (int): Number of lines to be deleted
    """
    for i in range(lines):
        print(f"{CURSOR_UP_ONE}{ERASE_LINE}", end="")

def delete_all_lines(searching_buffer:str, lines:int):
    """Delete the lines in the stdout
    
    Args:
        searching_buffer (str): the search buffer at the moment
        lines (int): quantity of lines to delete
    """
    print(CURSOR_BACKWARD*len(searching_buffer), end="")

    for index in range(0, lines+1):
        print(f"{ERASE_LINE}", end="")
        if index != lines:
            print(f"{CURSOR_UP_ONE}", end="")


def cursor_backwards(times:int=1):
    """Delete n times a characters
    
    Args:
        times (int): how many characters to delete
    """
    print(CURSOR_BACKWARD*times, end="")


def is_decodable(byte:bytes, encoding='utf-8'):
    """Checks if character is decodable
    
    Args:
        byte (bytes): character to check
        encoding (str): encoding format
    """
    try:
        byte.decode(encoding)
        return True
    except UnicodeDecodeError:
        return False
    

def clear_terminal():
    """Clears the terminal"""
    os.system("cls")
