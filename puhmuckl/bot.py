import os
import logging
import discord
from discord.ext import commands
from util import relative, config

# set path
logger = logging.getLogger("puhmuckl")
logger.debug("Working directory: "+str(os.path.dirname(__file__)))
relative.set_pwd(os.path.dirname(__file__))

# init config obj
#config = config.Config()

# Set log level - now use actual config
logger.setLevel(config.get_loglevel())
logging.basicConfig(level=logging.INFO)

# Checks config for valid .ini (and attempts to repair it or add new entries)
config.checkConfig()

# Intents, to access role members (Discord acces rights stuff)
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

# Create bot
bot = commands.Bot(command_prefix=config.get_config("CLIENT","prefix"), case_insensitive=True, intents=intents)

@bot.event
async def on_ready():
    '''This event is invoked when the bot is being logged in'''
    logger.info("We have logged in as %s", bot.user)

    logger.info("Trying to get version number...")
    try:
        with open(relative.make_relative("data","version"), "r", encoding="utf-8") as version_file:
            version_number = version_file.read()
            await bot.change_presence(activity=discord.Game(name=f"⏱️ {version_number}"))
            logging.info(f"Set version: {version_number}")

    except Exception as err:
        logger.warning("""
        Could not find version file. 
        Place a file named \"version\" in the data folder to display a version number in the bot presence.
        """)
        await bot.change_presence(activity=discord.Game(name=f"⏱️ unknown"))
        logger.warning(err)

    # Load modules from the cogs folder
    for cog in os.listdir(relative.make_relative("cogs")):
        if cog == "__pycache__":
            continue

        try:
            bot.load_extension(f"cogs.{cog}")
            logger.info(f"Loaded module {cog}")
        except Exception as err:
            logger.error(f"Failed to load module {cog}: {err}. Continuing")

# Launch bot
if __name__ == "__main__":
    bot.run(config.get_config("AUTHORIZATION","token"))
