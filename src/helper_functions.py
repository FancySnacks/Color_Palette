# Color Palette
# Created by Adrian Urbaniak / A-Rave-Mistake (2022)
# ----------
# Repo link: https://github.com/A-Rave-Mistake/Color_Palette
# Using GNU General Public License v3.0 - More info can be found in the 'LICENSE.md' file


from math import ceil
from random import randint
from typing import Tuple


cmyk_value = Tuple[float, float, float, float]
rgb_value = Tuple[int, int, int]
color = Tuple[rgb_value, str, str]


# check if string parameter is a valid HEX value
def is_hex_color(color: str) -> bool:
    import re
    check = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', color)
    return True if check else False

# check if string parameter is a valid RGB value
def is_rgb_color(color: rgb_value) -> bool:
    cases = [val for val in color if val in range(0, 255)]
    return all(cases)

def hex_to_rgb(hex_value: str) -> str:
    hex = hex_value.lstrip('#')
    return str(tuple(int(hex[i:i + 2], 16) for i in (0, 2, 4)))

def rgb_to_hex(rgb: rgb_value) -> str:
    # Legacy Code
    #rgb = (min(255, rgb[0]),min(255, rgb[1]),min(255, rgb[2]))
    #hex = bytes(rgb).hex()
    #return f'#{hex}'

    return '#%02x%02x%02x' % (rgb[0], rgb[1], rgb[2])

def cmyk_to_rgb(cmyk: cmyk_value) -> rgb_value:
    r = ceil((255 * (1 - cmyk[0]/100) * (1 - cmyk[3]/100)) + 1)
    g = ceil((255 * (1 - cmyk[1]/100) * (1 - cmyk[3]/100))+ 1)
    b = ceil((255 * (1 - cmyk[2]/100) * (1 - cmyk[3]/100))+ 1)
    return (r,g,b)

def str_to_rgb(rgb_str: (str, str, str)) -> rgb_value:
    return (int(rgb_str[0]), int(rgb_str[1]), int(rgb_str[2]))

def rgb_to_color(rgb: rgb_value) -> color:
    return (rgb, rgb_to_hex(rgb), "")

def random_rgb() -> rgb_value:
    return (randint(0, 255), randint(0, 255), randint(0, 255))

def get_shade(rgb_color: rgb_value, scalar: float = 1.0):
    cmyk = rgb_to_cmyk(rgb_color[0], rgb_color[1], rgb_color[2], scalar)
    return cmyk_to_rgb(cmyk)

def rgb_to_cmyk(r: int, g: int, b: int, scalar: float) -> cmyk_value:
    RGB_SCALE = 255
    CMYK_SCALE = 100

    if (r, g, b) == (0, 0, 0):
        # black
        return 0, 0, 0, CMYK_SCALE

    # rgb [0,255] -> cmy [0,1]
    c = 1 - r / RGB_SCALE
    m = 1 - g / RGB_SCALE
    y = 1 - b / RGB_SCALE

    # extract out k [0, 1]
    min_cmy = min(c, m, y)
    c = (c - min_cmy) / (1 - min_cmy)
    m = (m - min_cmy) / (1 - min_cmy)
    y = (y - min_cmy) / (1 - min_cmy)
    k = min_cmy

    # rescale to the range [0,CMYK_SCALE]
    return clamp_cmyk(c * CMYK_SCALE), clamp_cmyk(m * CMYK_SCALE), clamp_cmyk(y * CMYK_SCALE), clamp_cmyk((k * CMYK_SCALE) * scalar)

def clamp_cmyk(value: float):
    return float(min(ceil(value), 100))