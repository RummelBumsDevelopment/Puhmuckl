import logging
import configparser
import pathlib
import os

"""
This will handle configuration in this project.
config.ini is supposed to be generated and repaired in this class in case anything is missing.
"""

class Config:
    # $ProjectRoot/data/config.ini
    datafolder = os.path.join(pathlib.Path(__file__).parent.parent,"data")
    inipath = os.path.join(pathlib.Path(__file__).parent.parent,"data","config.ini")
    logfile = os.path.join(pathlib.Path(__file__).parent.parent,"data","puhmuckl.log")


    def generateConfig(self):
        # Generates entire configuration anew, this will CLEAR any previous configuration
        config = self.get_default_config()

        # Write config to file
        self.writeConfig(config)
        
        logging.info("Success! config.ini has been created!")
        logging.info("Change its parameters and restart the program.")
        exit()


    def checkConfig(self):
        # Check if config.ini is present, and whether it's incomplete
        
        # Check if 'data' folder is present
        if not os.path.exists(self.datafolder):
            logging.warning("Data folder doesen't exist, creating...")
            try:
                os.mkdir(self.datafolder)
            except Exception as e:
                logging.error("Failed to create data directory: "+ str(e))

        # Check if 'config.ini' is present
        if not os.path.exists(self.inipath):
            logging.warning("ini file doesen't exist, creating...")
            self.generateConfig()

        # Check if 'config.ini' is missing sections or keys
        defaultconfig = self.get_default_config()
        config = configparser.ConfigParser()
        config.read(self.inipath)

        # Adding missing sections/keys (Using defaultconfig as basefile)
        for section in defaultconfig.sections():
            # Adding sections
            if not section in config.sections():
                logging.warning("Section '"+str(section)+"' missing. Adding it now.")
                config.add_section(section)
            
            # Adding keys to sections
            for defaultkey in defaultconfig.items(section):
                currentKeys = []

                # Create list of current section keys
                for key in config.items(section):
                    currentKeys.append(key[0])

                if not defaultkey[0] in currentKeys:
                    logging.warning("Key '"+str(defaultkey[0])+"' missing. Adding it now.")
                    config[section][defaultkey[0]] = defaultkey[1]
                
        self.writeConfig(config)
        logging.info("Config check completed.")


    def writeConfig(self, config):
        # Write config to file
        try:
            with open(self.inipath, 'w') as configfile:
                config.write(configfile)
        except Exception as e:
            logging.error("Failed to write 'config.ini': "+ str(e))
            exit()


    def get_default_config(self):
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
    
    
    def get_config(self, category, key):
        # Calling just the string within the .ini without any checks
        config = configparser.ConfigParser()
        
        self.checkConfig()

        try:
            config.read(self.inipath)
            return config[category][key]
        except Exception as e:
            logging.error("Failed to read 'config.ini' "+ str(e))


    def get_loglevel(self):
        # Returns logging.<loglevel> object for configuration
        loglevel_input = str(self.get_config("LOGGING","loglevel")).lower()

        allowed_loglevels = {
            "debug" : logging.debug,
            "info" : logging.info,
            "warning" : logging.warning,
            "error" : logging.error,
            "critical" : logging.critical
        }

        try:
            return allowed_loglevels[loglevel_input]
        except Exception as e:
            logging.error("Failed to set configured loglevel. Defaulting to 'info'")
            return logging.info

# if config.py is run directly it will check and regenerate the 'config.ini'
logging.info("Checking 'config.ini'...")
Config().checkConfig()