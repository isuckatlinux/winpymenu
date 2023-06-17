""" Files that contains multiple math functions
"""

def clamp(num:int, min_value:int, max_value:int):
   """Function that clamps a number

    Args:
        num (int): Input value.
        min_value (int): Min value of the range.
        max_value (int): Max value of the range.
    Returns:
        int: Value clamped
   """
   return max(min(num, max_value), min_value)
