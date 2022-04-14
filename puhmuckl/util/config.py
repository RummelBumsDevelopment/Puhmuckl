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
    """Loads a config file and creates the parser object

    Returns:
        bool: True if the loading of the config was successful
    """
    logging.info("Trying to load config.ini...")

    try:
        with open(relative.make_relative("data/config.ini"), "r", encoding="utf-8") as configfile:
            config.read_file(configfile)
    except Exception as err:
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

        config.add_section("INGMAR")
        config["INGMAR"]["allowedChannels"] = ""

        os.mkdir(relative.make_relative("data"))
        with open(relative.make_relative("data/config.ini"), "w", encoding="utf-8") as configfile:
            config.write(configfile)

        return False

    return True

def get_client_config(key: str) -> str:
    """Returns a client config entry

    Args:
        key (str): Key to extract

    Returns:
        str: Value of the key
    """
    return config["CLIENT"][key]

def get_auth_config(key: str) -> str:
    """Returns a authorization config entry

    Args:
        key (str): Key to extract

    Returns:
        str: Value of the key
    """
    return config["AUTHORIZATION"][key]

def get_script_config(key: str) -> str:
    """Returns a script config entry

    Args:
        key (str): Key to extract

    Returns:
        str: Value of the key
    """
    return config["SCRIPT"][key]

def get_ingmar_allowedChannels():
    "Returns List of channels where Ingmar is allowed"
    return config["INGMAR"]["allowedChannels"].split(",")

def set_ingmar_allowedChannels(newChannel: str) -> str:
    """
    Adds new Channel to list of allowed channels
    """
    try:
        with open(relative.make_relative("data/config.ini"), "r", encoding="utf-8") as configfile:
            config.read_file(configfile)
    except Exception as e:
        print("Tja")
        return
   
    currentChannels = config["INGMAR"]["allowedChannels"]

    newChannel = str(newChannel)

    if newChannel in currentChannels:
        raise FileExistsError

    if len(currentChannels) != 0:
        currentChannels = currentChannels + ',' + newChannel
    else:
        currentChannels = newChannel

    config["INGMAR"]["allowedChannels"] = currentChannels

    with open(relative.make_relative("data/config.ini"), "w", encoding="utf-8") as configfile:
            config.write(configfile)

    return