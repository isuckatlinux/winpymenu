""" File that contains functions to detect key strokes in linux
"""
import os,time

if os.name.startswith("nt"):
    import msvcrt
elif os.name.startswith("posix"):
    import tty,termios,sys

class MultiPyKeyStrokes:
     
    _platform:str = os.name

    def init(self):
        """Initializes the library curses and configures settings in the terminal to make it usable in the way we want it
        """
        if MultiPyKeyStrokes._platform == "posix":
            self._old_settings = termios.tcgetattr(sys.stdin)
            tty.setcbreak(sys.stdin.fileno())

    def deinit(self):
        """Returns terminal to default settings and de-initialize the library
        """
        if MultiPyKeyStrokes._platform == "posix":
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self._old_settings)

    def readch(self) -> str:
        """Gets the character depending on the operating system
        """
        special_key = ""
        if self._platform == "nt": # Platform is windows
            key = msvcrt.getch() # Get the key pressed
            if key == b'\xe0':  # It's a special key
                special_key = key
                key = msvcrt.getch()
                return special_key, key # Get the actual key pressed, returns None if none key has been pressed
            else:
                return key

        elif self._platform == "posix": # Platform is posix
            key = sys.stdin.read(1) # Get the key pressed
            special_key = ""
            if key == '\x1b':   # It's a special key
                special_key = key
                key = sys.stdin.read(2) # Get the actual key pressed, returns None if none key has been pressed
                return special_key, key
            return key
    
    def specialkey(self, key):
        return key[0] == '\x1b' or key[0] == b'\xe0'
    
    def getkey(self, key):
        if self.specialkey(key):
            if key[1] == b'H' or key[1] == '[A': # Arrow up key
                return "KEY_UP"
            elif key[1] == b'P' or key[1] == '[B': # Arrow down key
                return "KEY_DOWN"
        elif key == b'\r' or key == '\n':
            return "RETURN"
        elif key == b'/' or key == '/':
            return "SLASH"
        elif key == b'\x08' or key == '\x7f':
            return "BACKSPACE"
        else:
            return key

    def kbhit(self, key) -> bool:
        """Checks if the key provided is a valid key, if not, it means none key has been pressed
        """
        if os.name.startswith("nt"):
                return key is not None
        elif os.name.startswith("posix"):
            if self.specialkey(key):
                return key[1] != ""
            else:
                return key != ""