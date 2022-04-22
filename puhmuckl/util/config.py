import logging
import configparser
import os
from util import relative

# Use logger from "main"
log = logging.getLogger(__name__)

"""
This will handle configuration in this project.
config.ini is supposed to be generated and repaired in this class in case anything is missing.

Please use get_config() if you only need the string in the ini
"""


def generateConfig():
    # Generates entire configuration anew, this will CLEAR any previous configuration
    config = get_default_config()

    # Write config to file
    writeConfig(config)
    
    log.info("Success! config.ini has been created!")
    log.info("Change its parameters and restart the program.")
    exit()


def checkConfig():
    # Check if config.ini is present, and whether it's incomplete
    
    # Check if 'data' folder is present
    if not os.path.exists(get_datafolder()):
        log.warning("Data folder doesen't exist, creating...")
        try:
            os.mkdir(get_datafolder())
        except Exception as e:
            log.error("Failed to create data directory: "+ str(e))

    # Check if 'config.ini' is present
    if not os.path.exists(get_inipath()):
        log.warning("ini file doesen't exist, creating...")
        generateConfig()

    # Check if 'config.ini' is missing sections or keys
    defaultconfig = get_default_config()
    config = configparser.ConfigParser()
    config.read(get_inipath())

    # Adding missing sections/keys (Using defaultconfig as basefile)
    for section in defaultconfig.sections():
        # Adding sections
        if not section in config.sections():
            log.warning("Section '"+str(section)+"' missing. Adding it now.")
            config.add_section(section)
        
        # Adding keys to sections
        for defaultkey in defaultconfig.items(section):
            currentKeys = []

            # Create list of current section keys
            for key in config.items(section):
                currentKeys.append(key[0])

            if not defaultkey[0] in currentKeys:
                log.warning("Key '"+str(defaultkey[0])+"' missing. Adding it now.")
                config[section][defaultkey[0]] = defaultkey[1]
            
    writeConfig(config)
    log.info("Config check completed.")


def writeConfig(config):
    # Write config to file
    try:
        with open(get_inipath(), 'w') as configfile:
            config.write(configfile)
    except Exception as e:
        log.error("Failed to write 'config.ini': "+ str(e))
        exit()


def get_default_config():
    # This is where you can define what the config.ini is supposed to look like
    # DO NOT SET ANY API KEYS OR PASSWORDS AS DEFAULT
    config = configparser.ConfigParser()

    config['AUTHORIZATION'] = {
        "token" : "",
        "wolframalpha" : ""
    }

    config['CLIENT'] = {
        "prefix" : "?"
    }

    config['SCRIPT'] = {
        "loglevel" : "info"
    }

    config['ZENSURSULA'] = {
        "censoredwords" : "",
        "uncensoredchannels" : "",
    }
    return config


def get_config(category, key):
    # Calling just the string within the .ini without any checks
    config = configparser.ConfigParser()

    try:
        config.read(get_inipath())
        return config[category][key]
    except Exception as e:
        log.error("Failed to read 'config.ini' "+ str(e))


def get_config_object():
    # Returns entire config object for further manipulation
    config = configparser.ConfigParser()

    try:
        config.read(get_inipath())
        return config
    except Exception as e:
        log.error("Failed to read 'config.ini' "+ str(e))


def get_datafolder():
    datafolder = relative.make_relative("data")
    return datafolder


def get_inipath():
    inipath = relative.make_relative("data","config.ini")
    return inipath


def get_logfile():
    logfile = relative.make_relative("data","puhmuckl.log")
    return logfile


def get_loglevel():
    # Returns log.<loglevel> object for configuration
    loglevel_input = str(get_config("SCRIPT","loglevel")).lower()

    allowed_loglevels = {
        "debug" : logging.DEBUG,
        "info" : logging.INFO,
        "warning" : logging.WARNING,
        "error" : logging.ERROR,
        "critical" : logging.CRITICAL
    }

    try:
        return allowed_loglevels[loglevel_input]
    except Exception as e:
        log.error("Failed to set configured loglevel. Defaulting to 'debug'")
        return logging.DEBUG


def set_config(category, key, value):
    # change config option
    config = get_config_object()
    config[category][key] = value
    writeConfig(config)