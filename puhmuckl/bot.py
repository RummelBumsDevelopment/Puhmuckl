from settings import BOT_PREFIX, BOT_TOKEN
import os
import logging
from discord.ext import commands

bot = commands.Bot(command_prefix=BOT_PREFIX, case_insensitive=True)
pwd = os.path.dirname(__file__)

@bot.event
async def on_ready():
    logging.basicConfig(level=logging.DEBUG)
    logging.info(f"We have logged in as {bot.user}")

    for cog in os.listdir(os.path.join(pwd, "./cogs")):
        if cog.endswith(".py"):
            cog_name = cog[:-3]
            try:
                bot.load_extension(f"cogs.{cog_name}")
                logging.info(f"Loaded module {cog_name}")
            except Exception as e:
                logging.error(f"Failed to load module {cog_name}. Continuing")
                pass

bot.run(BOT_TOKEN)