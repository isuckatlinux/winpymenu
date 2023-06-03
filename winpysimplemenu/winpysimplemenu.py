from dataclasses import dataclass, field
import msvcrt
from ..winpyterminal import print_lines, delete_lines
from ..winpycolors import WinPyColors, WinPyStyles, ENDC
from ..winpymath import clamp

@dataclass
class WinPySimpleMenu:
    options:list[str]
    default_option:int = 0
    prechar:str = "> "
    clear_terminal:bool = False
    clear_on_exit:bool = True
    selected_color:WinPyColors = ""
    selected_style:WinPyStyles = WinPyStyles.UNDERLINE
    _selected_option:int = default_option
    _lines_printed:int = 0

    @property
    def _pritable_options(self):
        temp_option:str
        temp_printable_options:list = []
        for index, option in enumerate(self.options):
            temp_option = option
            if index == self._selected_option:
                temp_option = self.selected_color + self.selected_style + temp_option
            temp_option = self.prechar + temp_option + ENDC
            temp_printable_options.append(temp_option)
        return temp_printable_options

    def show(self):
        self._lines_printed = print_lines(self._pritable_options)
        while True:
            if msvcrt.kbhit():
                key = msvcrt.getch()
                if key == b'\xe0': # tecla especial
                    arrow_key = msvcrt.getch()
                    if arrow_key == b'H':
                        self._selected_option -= 1
                    elif arrow_key == b'P':
                        self._selected_option += 1
                    else:
                        print(arrow_key)
                    self._selected_option = clamp(self._selected_option, 0, len(self.options)-1)
                elif key == b'\r':
                    return self._selected_option

                delete_lines(self._lines_printed)
                self._lines_printed = print_lines(self._pritable_options)
