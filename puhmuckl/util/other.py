import re

def is_emoji(word: str) -> bool:
    '''Checks if string is a discord emoji'''

    if re.search("<a?:.+?:\d{18}>", word) is not None:
        print(f"{word} is an emoji")
        return True
    else:
        print(f"{word} is NOT an emoji")
        return False