from dataclasses import dataclass
import msvcrt
from mathfpy import clamp
import os
from iomethods import delete_stdout_lines


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
    selected:int = 0
    prechar:str = "> "
    clear_on_exit:bool = True
    _lines_printed:int = 0
    _write:bool = True

    def show(self):

        while True:
            if msvcrt.kbhit():
                key = msvcrt.getch()
                if key == b'H':
                    self.selected -= 1
                elif key == b'P':
                    self.selected += 1
                elif key == b'\r':
                    delete_stdout_lines(self._lines_printed) if self.clear_on_exit  else None
                    return self.selected

                self._write = True
            self.selected = clamp(self.selected, 0, len(self.options)-1)

            printable_options:list[str] = []
            for index, option in enumerate(self.options):

                if index == self.selected:
                    printable_options.append(f"{self.prechar}{bcolors.UNDERLINE}{option}{bcolors.ENDC}")
                else:
                    printable_options.append(f"{self.prechar}{option}")
            
            if self._write:
                delete_stdout_lines(self._lines_printed)

                self._lines_printed = 0
                for poption in printable_options:
                    print(poption)
                    self._lines_printed += 1
                
                self._write = False






menu = WinPyMenu(options=["aaa", "bbb", "ccc", "dsfnmkk", "dfpkdjk"])

option = menu.show()

print(option)