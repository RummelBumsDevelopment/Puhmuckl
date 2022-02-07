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

def make_relative(path: str) -> str:
    """Makes a relative path relative to the pwd

    Args:
        path (str): Generic relative path

    Returns:
        str: Path relative to pwd
    """
    return os.path.join(PWD, path)