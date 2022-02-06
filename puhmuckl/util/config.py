"""
Contains the configs of the bots ini file
"""

from configparser import ConfigParser
import os
import logging
from util import relative

config = ConfigParser()

def load_config(file: str) -> bool:
    logging.info("Trying to load config.ini...")

    try:
        with open(relative.make_relative("data/config.ini"), "r") as configfile:
            config.read_file(configfile)
    except:
        logging.error("Could not open config.ini, please look inside the data folder, enter credentials and restart the bot")
        
        config.add_section("AUTHORIZATION")
        config["AUTHORIZATION"]["token"] = "Bot Token"

        config.add_section("CLIENT")
        config["CLIENT"]["prefix"] = ";"

        config.add_section("SCRIPT")
        config["SCRIPT"]["logLevel"] = "INFO"

        os.mkdir(relative.make_relative("data"))
        with open(relative.make_relative("data/config.ini"), "w") as configfile:
            config.write(configfile)

        return False

    return True

def get_client_config(key: str) -> str:
    return config["CLIENT"][key]

def get_auth_config(key: str) -> str:
    return config["AUTHORIZATION"][key]

def get_script_config(key: str) -> str:
    return config["SCRIPT"][key]