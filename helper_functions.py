# check if string parameter is a valid color in HEX code
def is_hex_color(color: str) -> bool:
    import re
    check = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', color)
    return True if check else False

def hex_to_rgb(hex_value: str) -> str:
    hex = hex_value.lstrip('#')
    return str(tuple(int(hex[i:i + 2], 16) for i in (0, 2, 4)))