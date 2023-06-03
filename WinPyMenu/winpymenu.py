from dataclasses import dataclass, field
import msvcrt
from mathfpy import clamp
import os
from iomethods import delete_stdout_lines
import string as stringgg
import re

PRINTABLE_BYTES = [x.encode("utf-8") for x in stringgg.printable]

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


@dataclass
class WinPyMenu:
    options:list[str]
    default_selection:int = 0
    prechar:str = "> "
    multiselect:bool = False
    multiselect_prechar_selected:str = "[*] "
    multiselect_prechar_unselected:str = "[ ] "
    clear_on_exit:bool = True
    _lines_printed:int = 0
    _write:bool = True
    _multiselected:list[int] = field(default_factory=list)
    _selected:int = 0
    
    # Searching
    _searching:bool = False
    _searching_buffer:str = ""



    def show(self):
        self._selected = self.default_selection
        while True:
            if msvcrt.kbhit():
                key = msvcrt.getch()
                if key == b'H':
                    self._selected -= 1
                elif key == b'P':
                    self._selected += 1
                elif key == b'/' and not self._searching:
                    self._searching = True
                    self._searching_buffer = "/"
                elif self._searching and key in PRINTABLE_BYTES:
                    self._searching_buffer += key.decode()
                elif self._searching and key == b'\x08':
                    self._searching_buffer = self._searching_buffer[:-1]
                    self._searching = False if self._searching_buffer == "" else True
                elif key == b'\t' and self.multiselect:
                    self._multiselected.remove(self._selected) if self._selected in self._multiselected else self._multiselected.append(self._selected)
                elif key == b'\r':
                    delete_stdout_lines(self._lines_printed) if self.clear_on_exit else None
                    if not self.multiselect:
                        return self._selected
                    else:
                        self._multiselected.sort()
                        return self._multiselected

                self._write = True
            self._selected = clamp(self._selected, 0, len(self.options)-1)

            printable_options:list[str] = []
            temp_options = self.options[:]
            if self._searching:
                patron_regex = re.compile(self._searching_buffer[1:])
                temp_options = [x for x in temp_options if re.match(patron_regex, x)]

            for index, option in enumerate(temp_options):
                string = ""
                string += self.multiselect_prechar_selected if self.multiselect and index in self._multiselected else ""
                string += self.multiselect_prechar_unselected if self.multiselect and index not in self._multiselected else ""
                string += self.prechar if not self.multiselect else ""
                string += bcolors.UNDERLINE if index == self._selected else ""
                string += f"{option}{bcolors.ENDC}"
                printable_options.append(string)
            
            if self._write:
                delete_stdout_lines(self._lines_printed)

                self._lines_printed = 0
                for poption in printable_options:
                    print(poption)
                    self._lines_printed += 1
                
                if self._searching:
                    print()
                    print(self._searching_buffer)
                    self._lines_printed += 2
                
                self._write = False

            




menu = WinPyMenu(options=["aaa", "bbb", "abc"])

option = menu.show()

print(option)

import unicurses