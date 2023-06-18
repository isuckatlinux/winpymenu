from enum import Enum
import os

class Platform(Enum):
    WINDOWS = "WINDOWS"
    LINUX = "LINUX"

def get_platform() -> Platform:
    if os.name.startswith("nt"):
        return Platform.WINDOWS
    elif os.name.startswith("posix"):
        return Platform.LINUX

