
CURSOR_UP_ONE = '\x1b[1A'
ERASE_LINE = '\x1b[2K'

def delete_stdout_lines(lines:int):
    """ Delete a number of lines from stodut

    Args:
        lines (int): Number of lines to be deleted
    """
    for i in range(lines):
        print(f"{CURSOR_UP_ONE}{ERASE_LINE}{CURSOR_UP_ONE}")
