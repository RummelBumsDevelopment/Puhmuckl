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

        config.add_section("ZENSURSULA")
        config["ZENSURSULA"]["uncensoredChannels"] = ""
        config["ZENSURSULA"]["censoredWords"] = ""

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


def get_censoredWords():
    # returns list of censored words

    return config["ZENSURSULA"]["censoredWords"].split(",")


def get_uncensoredChannels():
    "Returns List of channels where no censorship takes place"
    return config["ZENSURSULA"]["uncensoredChannels"].split(",")


def set_channelCensorship(newChannel: str, censorship) -> str:
    """
    Adds new Channel to list of allowed channels
    """

    # pull list of currently uncensored channels
    uncensoredChannels = config["ZENSURSULA"]["uncensoredChannels"].split(",")

    if censorship:
        # channel will be censored
        if str(newChannel) in uncensoredChannels:
            uncensoredChannels.remove(str(newChannel))
        else:
            raise FileExistsError
    else:
        # channel will be uncensored
        if str(newChannel) in uncensoredChannels:
            raise FileExistsError
        
        uncensoredChannels.append(str(newChannel))

    # Make list string again
    config["ZENSURSULA"]["uncensoredChannels"] = ",".join(uncensoredChannels)
    
    # Write that shit to the .ini file
    with open(relative.make_relative("data/config.ini"), "w", encoding="utf-8") as configfile:
            config.write(configfile)
    return