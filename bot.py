from settings import BOT_PREFIX, BOT_TOKEN
import os
from discord.ext import commands

bot = commands.Bot(command_prefix=BOT_PREFIX, case_insensitive=True)

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

    for cog in os.listdir("./cogs"):
        if cog.endswith(".py"):
            cog_name = cog[:-3]
            try:
                bot.load_extension(f"cogs.{cog_name}")
                print(f"Loaded module {cog_name}")
            except Exception as e:
                print(f"Failed to load module {cog_name}")
                pass

bot.run(BOT_TOKEN)