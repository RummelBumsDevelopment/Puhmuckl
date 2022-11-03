import re

def is_emoji(word: str) -> bool:
    '''Checks if string is a discord emoji'''

    if re.search("<a?:.+?:\d{18}>", word):
        return True
    else:
        return False