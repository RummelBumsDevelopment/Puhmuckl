import re

def deminecraftify(string: str) -> str:
    return re.sub(r"§[a-z,0-9]", "", string)