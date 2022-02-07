import os
import logging
import discord
from discord.ext import commands
from util import relative, config

# Set log level
log_level_dict = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR
}
logging.basicConfig(level=logging.INFO)

# Set up paths, config and logging
relative.set_pwd(os.path.dirname(__file__))
if not config.load_config(relative.make_relative("data/config.ini")):
    exit(-1)

logging.getLogger().setLevel(log_level_dict[config.get_script_config("logLevel")])

# Create bot
bot = commands.Bot(command_prefix=config.get_client_config("prefix"), case_insensitive=True)

@bot.event
async def on_ready():
    logging.info(f"We have logged in as {bot.user}")

    logging.info("Trying to get version number...")
    try:
        with open(relative.make_relative("data/version"), "r") as version_file:
            version_number = version_file.read()
            await bot.change_presence(activity=discord.Game(name=f"⏱️ {version_number}"))
    except Exception as e:
        logging.warning("Could not find version file. Place a file named \"version\" in the data folder to display a version number in the bot presence")
        logging.warning(e)

    # Load modules from the cogs folder
    for cog in os.listdir(relative.make_relative("cogs")):
        if cog == "__pycache__":
            continue
        
        try:
            bot.load_extension(f"cogs.{cog}")
            logging.info(f"Loaded module {cog}")
        except Exception as e:
            logging.error(f"Failed to load module {cog}: {e}. Continuing")
            pass

# Launch bot
if __name__ == "__main__":
    bot.run(config.get_auth_config("token"))