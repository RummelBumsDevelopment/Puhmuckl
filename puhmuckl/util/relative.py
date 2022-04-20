"""
Makes paths relative to the bot.py
"""
import os

PWD = ""

def set_pwd(path: str):
    """Sets the new working directory

    Args:
        path (str): The new working directory
    """
    global PWD
    PWD = path

def make_relative(*args):
    # takes multiple strings and combines them into a new path

    result = PWD

    for item in args:
        result = os.path.join(result,item)

    return result