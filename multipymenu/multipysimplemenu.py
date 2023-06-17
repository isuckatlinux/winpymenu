from dataclasses import dataclass, field
import os
import string
import re
from .multipyterminal import print_lines, delete_lines, delete_all_lines, cursor_backwards, is_decodable, clear_terminal
from .multipycolors import MultiPyColors, MultiPyStyles, ENDC
from .multipymath import clamp
from .multipykeystrokes import MultiPyKeyStrokes


@dataclass
class MultiPySimpleMenu:
    """ Simple CLI menu for windows

    Args:
        options (list[str]): List of the options for the menu
        default_option (int): Deafult option that will be highlihged
        prechar (str): Prechar for the options. Defaults to "> "
        clear_on_exit (bool): Clear console in exit of the menu. Defaults on True
        selected_color (MultiPyColors): Color of the selected option. Defaults to None
        selected_style (MultiPyStyles): Font style pf the seletect option. Defaults to None
    
    """
    options:list[str]
    default_option:int = 0
    prechar:str = "> "
    clear_on_exit:bool = True
    selected_color:MultiPyColors = ""
    selected_style:MultiPyStyles = MultiPyStyles.UNDERLINE
    
    _selected_option:int = default_option
    _searching_buffer:str = ""

    # Size in lines of the terminal
    _terminal_last_line_size:int = os.get_terminal_size().lines

    # Size in columns of the terminal
    _terminal_last_column_size:int = os.get_terminal_size().columns

    # Operating system
    _platform:str = os.name

    
    @property
    def _printable_options(self):
        """"Return the formatted options to print"""
        temp_option:str
        temp_printable_options:list = []

        available_options:list[str] = []

         # Checks if searching is active, that is to say, user has typed at least /
        if self._searching:
            # Filter options based on search pattern
            for option in self.options:
                if re.match(re.escape(self._searching_buffer[1:]), option):
                    available_options.append(option)
        else:
            available_options = self.options[:]

        # Adds the styles selected to the options
        for index, option in enumerate(available_options):
            temp_option = option
            if index == self._selected_option:
                temp_option = self.selected_color + self.selected_style + temp_option
            temp_option = self.prechar + temp_option + ENDC
            temp_printable_options.append(temp_option)
        return temp_printable_options
    
    @property
    def _terminal_resized(self) -> bool:
        """Check if the terminal has been resized"""
        return os.get_terminal_size().lines != self._terminal_last_line_size or os.get_terminal_size().columns != self._terminal_last_column_size

    @property
    def _searching(self) -> bool:
        """Check if searching is active by checking the length of the searching buffer"""
        return len(self._searching_buffer) > 0

    def show(self):
        """ Displays the menu and handles user interactions.

            This method clears the terminal and prints the menu options. It continuously listens for keyboard input from the user.
            The menu supports arrow key navigation, search functionality, and the Enter key to select an option.

            Returns:
                int: The index of the selected option.
                clear_terminal()
                print_lines(self._printable_options, self._searching_buffer)
        """

        kshandler = MultiPyKeyStrokes()
        kshandler.init()

        print_lines(self._printable_options, self._searching_buffer)

        try:
            while True:
                # Checks if the terminal has been resized
                if self._terminal_resized:
                    self._terminal_last_line_size = os.get_terminal_size().lines
                    self._terminal_last_column_size = os.get_terminal_size().columns
                    clear_terminal()
                    print_lines(self._printable_options, self._searching_buffer)

                # Checks for a key stroke
                key = kshandler.readch()

                """kshandler.deinit()
                print(repr(key))
                print(repr(kshandler.getkey(key)))
                exit()"""
                
                if kshandler.kbhit(key):
                    if kshandler.specialkey(key): # If it's a special key
                        if kshandler.getkey(key) == "KEY_UP": # Arrow up key
                            self._selected_option -= 1
                        elif kshandler.getkey(key) == "KEY_DOWN": # Arrow down key
                            self._selected_option += 1

                        # Keep the selected option within the valid range
                        self._selected_option = clamp(self._selected_option, 0, len(self._printable_options)-1)
                    
                    # Checks for the return key
                    elif kshandler.getkey(key) == "RETURN":
                        if self.clear_on_exit:
                            # Delete all lines including the searching buffer
                            delete_all_lines(self._searching_buffer, self._terminal_last_line_size)
                        else:
                            # Delete lines below the menu options
                            delete_lines(lines=os.get_terminal_size().lines - len(self.options)-1)
                        return self._selected_option
                        
                    # Checks if key / has been pressed to start searching
                    elif kshandler.getkey(key) == "SLASH" and not self._searching:
                        self._searching_buffer = "/"
                        
                        # Checks if user is searching
                    elif self._searching:
                        if kshandler.getkey(key) == "BACKSPACE": # backspace key
                            char_to_remove = self._searching_buffer[-1]
                            self._searching_buffer = self._searching_buffer[:-1]
                            if char_to_remove.encode() == b'\t': # In case character to be deleted is a TAB
                                cursor_backwards(times=7)
                            else:
                                cursor_backwards()

                        # If key added is decodable and is printable, add it to the buffer
                        elif self._platform == "nt" and is_decodable(key) and key.decode() in string.printable:
                            self._searching_buffer += key.decode()
                        
                        elif self._platform == "posix" and key in string.printable:
                            self._searching_buffer += key

                    # Keep the selected option within the valid range
                    self._selected_option = clamp(self._selected_option, 0, len(self._printable_options)-1)
                        
                    delete_all_lines(self._searching_buffer, self._terminal_last_line_size)
                    print_lines(self._printable_options, self._searching_buffer)
        finally:
            kshandler.deinit()
