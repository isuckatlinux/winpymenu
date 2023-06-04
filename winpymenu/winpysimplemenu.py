from dataclasses import dataclass, field
import msvcrt
from .winpyterminal import print_lines, delete_lines, delete_all_lines, cursor_backwards, is_decodable, clear_terminal
from .winpycolors import WinPyColors, WinPyStyles, ENDC
from .winpymath import clamp
import os
import string
import re


@dataclass
class WinPySimpleMenu:
    """ Simple CLI menu for windows

    Args:
        options (list[str]): List of the options for the menu
        default_option (int): Deafult option that will be highlihged
        prechar (str): Prechar for the options. Defaults to "> "
        clear_on_exit (bool): Clear console in exit of the menu. Defaults on True
        selected_color (WinPyColors): Color of the selected option. Defaults to None
        selected_style (WinPyStyles): Font style pf the seletect option. Defaults to None
    
    """
    options:list[str]
    default_option:int = 0
    prechar:str = "> "
    clear_on_exit:bool = True
    selected_color:WinPyColors = ""
    selected_style:WinPyStyles = WinPyStyles.UNDERLINE
    _selected_option:int = default_option

    _searching_buffer:str = ""

    _terminal_last_line_size:int = os.get_terminal_size().lines
    _terminal_last_column_size:int = os.get_terminal_size().columns

    @property
    def _pritable_options(self):
        temp_option:str
        temp_printable_options:list = []

        available_options:list[str] = []
        for option in self.options:
            if re.match(re.escape(self._searching_buffer[1:]), option):
                available_options.append(option)

        for index, option in enumerate(available_options):
            temp_option = option
            if index == self._selected_option:
                temp_option = self.selected_color + self.selected_style + temp_option
            temp_option = self.prechar + temp_option + ENDC
            temp_printable_options.append(temp_option)
        return temp_printable_options
    
    @property
    def _terminal_resized(self):
        return os.get_terminal_size().lines != self._terminal_last_line_size or os.get_terminal_size().columns != self._terminal_last_column_size

    @property
    def _searching(self) -> bool:
        return len(self._searching_buffer) > 0


    def show(self):
        clear_terminal()
        print_lines(self._pritable_options, self._searching_buffer)
        while True:
            if self._terminal_resized:
                self._terminal_last_line_size = os.get_terminal_size().lines
                self._terminal_last_column_size = os.get_terminal_size().columns
                clear_terminal()
                print_lines(self._pritable_options, self._searching_buffer)

            if msvcrt.kbhit():
                key = msvcrt.getch()
                if key == b'\xe0': # tecla especial
                    special_key = msvcrt.getch()
                    if special_key == b'H':
                        self._selected_option -= 1
                    elif special_key == b'P':
                        self._selected_option += 1
                    self._selected_option = clamp(self._selected_option, 0, len(self._pritable_options)-1)
                elif key == b'\r':
                    delete_all_lines(self._searching_buffer, self._terminal_last_line_size)
                    return self._selected_option
                elif key == b'/' and not self._searching:
                    self._searching_buffer = "/"
                elif self._searching:
                    if key == b'\x08':
                        char_to_remove = self._searching_buffer[-1]
                        self._searching_buffer = self._searching_buffer[:-1]
                        if char_to_remove.encode() == b'\t':
                            cursor_backwards(times=6)
                        cursor_backwards()

                    elif is_decodable(key) and key.decode() in string.printable:
                        self._searching_buffer += key.decode()

                self._selected_option = clamp(self._selected_option, 0, len(self._pritable_options)-1)
                delete_all_lines(self._searching_buffer, self._terminal_last_line_size)
                print_lines(self._pritable_options, self._searching_buffer)
