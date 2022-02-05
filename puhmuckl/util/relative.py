"""
Makes paths relative to the bot.py
"""

import os

pwd = ""

def set_pwd(path: str):
    global pwd
    pwd = path

def make_relative(path: str):
    return os.path.join(pwd, path)