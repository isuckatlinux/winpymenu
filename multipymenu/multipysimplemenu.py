from dataclasses import dataclass, field
import msvcrt
import os
import string
import re
from .multipyterminal import print_lines, delete_lines, delete_all_lines, cursor_backwards, is_decodable, clear_terminal
from .multipycolors import MultiPyColors, MultiPyStyles, ENDC
from .multipymath import clamp


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

    
    @property
    def _printable_options(self):
        """"Return the formatted options to print"""
        temp_option:str
        temp_printable_options:list = []

        available_options:list[str] = []

        # If the user is searching at the moment, filter the options using the searching buffer
        if self._searching:
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
        """Returns true if the user is searching"""
        return len(self._searching_buffer) > 0

    def show(self):
        """Shows the printable options"""
        clear_terminal()
        print_lines(self._printable_options, self._searching_buffer)

        while True:
            # Checks if the terminal has been resized
            if self._terminal_resized:
                self._terminal_last_line_size = os.get_terminal_size().lines
                self._terminal_last_column_size = os.get_terminal_size().columns
                clear_terminal()
                print_lines(self._printable_options, self._searching_buffer)

            # Checks for a key stroke
            if msvcrt.kbhit():
                key = msvcrt.getch()
                if key == b'\xe0': # If it's a special key
                    special_key = msvcrt.getch()
                    if special_key == b'H': # Arrow up key
                        self._selected_option -= 1
                    elif special_key == b'P': # Arrow down key
                        self._selected_option += 1
                    self._selected_option = clamp(self._selected_option, 0, len(self._printable_options)-1)
                
                # Checks for the return key
                elif key == b'\r':
                    if self.clear_on_exit:
                        delete_all_lines(self._searching_buffer, self._terminal_last_line_size)
                    else:
                        delete_lines(lines=os.get_terminal_size().lines - len(self.options)-1)
                    return self._selected_option
                
                # Checks if key / has been pressed
                elif key == b'/' and not self._searching:
                    self._searching_buffer = "/"
                
                # Checks if user is searching
                elif self._searching:
                    if key == b'\x08': # backspace key
                        char_to_remove = self._searching_buffer[-1]
                        self._searching_buffer = self._searching_buffer[:-1]
                        if char_to_remove.encode() == b'\t': # In case character to be deleted is a TAB
                            cursor_backwards(times=7)
                        else:
                            cursor_backwards()

                    # If key added is decodable and is printable, add it to the buffer
                    elif is_decodable(key) and key.decode() in string.printable:
                        self._searching_buffer += key.decode()

                # Checks the selected option
                self._selected_option = clamp(self._selected_option, 0, len(self._printable_options)-1)
                delete_all_lines(self._searching_buffer, self._terminal_last_line_size)
                print_lines(self._printable_options, self._searching_buffer)