import random

# check if string parameter is a valid HEX value
def is_hex_color(color: str) -> bool:
    import re
    check = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', color)
    return True if check else False

# check if string parameter is a valid RGB value
def is_rgb_color(color: tuple) -> bool:
    cases = [val for val in color if val in range(0, 255)]
    return all(cases)

def hex_to_rgb(hex_value: str) -> str:
    hex = hex_value.lstrip('#')
    return str(tuple(int(hex[i:i + 2], 16) for i in (0, 2, 4)))

def rgb_to_hex(rgb_value: tuple) -> str:
    return '#%02x%02x%02x' % (rgb_value[0], rgb_value[1], rgb_value[2])

def random_rgb() -> tuple:
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))