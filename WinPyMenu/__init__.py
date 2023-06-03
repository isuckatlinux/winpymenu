from winpymenu import WinPyMenu

import platform

if platform.system() != "Windows":
    raise Exception("This libray is only avaiable on windows")