"""
Makes paths relative to the bot.py
"""
import os

PWD = ""

"""Sets the new working directory
"""
def set_pwd(path: str):
    global PWD
    PWD = path

"""Makes a relative path relative to the pwd
"""
def make_relative(path: str):
    return os.path.join(PWD, path)