"""
Contains the configs of the bots ini file
"""
from configparser import ConfigParser
import os
import logging
from util import relative

config = ConfigParser()

"""Loads a config file and creates the parser object
"""
def load_config() -> bool:
    logging.info("Trying to load config.ini...")

    try:
        with open(relative.make_relative("data/config.ini"), "r", encoding="utf-8") as configfile:
            config.read_file(configfile)
    except:
        logging.error("""
            Could not open config.ini, please look inside the data folder, 
            enter credentials and restart the bot
            """)
        
        config.add_section("AUTHORIZATION")
        config["AUTHORIZATION"]["token"] = "Bot Token"

        config.add_section("CLIENT")
        config["CLIENT"]["prefix"] = ";"

        config.add_section("SCRIPT")
        config["SCRIPT"]["logLevel"] = "INFO"

        os.mkdir(relative.make_relative("data"))
        with open(relative.make_relative("data/config.ini"), "w", encoding="utf-8") as configfile:
            config.write(configfile)

        return False

    return True

"""Returns a client config entry
"""
def get_client_config(key: str) -> str:
    return config["CLIENT"][key]

"""Returns an authorization config entry
"""
def get_auth_config(key: str) -> str:
    return config["AUTHORIZATION"][key]

"""Returns a script config entry
"""
def get_script_config(key: str) -> str:
    return config["SCRIPT"][key]
