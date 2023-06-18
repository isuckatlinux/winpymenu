import os
from typing import Union
from .special_keys import SpecialKeys
from .multiplatform import get_platform, Platform

platform = get_platform()
if platform == Platform.WINDOWS:
    import msvcrt
elif platform == Platform.LINUX:
    import tty,termios,sys


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
    for _ in range(count+1, os.get_terminal_size().lines):
        print()
    
    # Prints the searching buffer.
    print(searching_buffer, end="", flush=True)

def delete_lines(lines:int):
    """ Delete a number of lines from stodut

    Args:
        lines (int): Number of lines to be deleted
    """
    for _ in range(lines):
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


class MultiPyKeyStrokes:
     
    def init(self):
        """Initializes the library curses and configures settings in the terminal to make it usable in the way we want it
        """
        if platform == Platform.LINUX:
            self._old_settings = termios.tcgetattr(sys.stdin)
            tty.setcbreak(sys.stdin.fileno())

    def deinit(self):
        """Returns terminal to default settings and de-initialize the library
        """
        if platform == Platform.LINUX:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self._old_settings)

    def readch(self) -> Union[str, SpecialKeys]:
        """Gets the character depending on the operating system
        """
        if platform == Platform.WINDOWS:
            key = msvcrt.getch() # Get the key pressed
            if key == b'\xe0':  # It's a special key
                key = msvcrt.getch()
                if key == b'H':
                    return SpecialKeys.ARROW_UP
                elif key == b'P':
                    return SpecialKeys.ARROW_DOWN
            elif key == b'\r':
                return SpecialKeys.INTRO
            elif key == b'\x08':
                return SpecialKeys.BACKSPACE
            elif key == b'/':
                return SpecialKeys.SLASH
            elif is_decodable(key):
                return key.decode()

        elif platform == Platform.LINUX: # Platform is posix
            key = sys.stdin.read(1) # Get the key pressed
            if key == '\x1b':   # It's a special key
                key = sys.stdin.read(2) # Get the actual key pressed, returns None if none key has been pressed
                if key == '[A':
                    return SpecialKeys.ARROW_UP
                elif key == '[B':
                    return SpecialKeys.ARROW_DOWN                
            elif key == '\n':
                return SpecialKeys.INTRO
            elif key == '\x7f':
                return SpecialKeys.BACKSPACE
            elif key == "/":
                return SpecialKeys.SLASH
            return key