"""
Allows pulling current version from version file
Only neccessary when last pull didn't change the bot's code
"""
from discord.ext import commands
from util import relative
import logging

class Version(commands.Cog):
    """Version cog"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="version", help="prints current commit #")
    async def echo(self, ctx: commands.context, *args):
        """Echo command implementation
        Args:
            ctx (commands.context): Context in which the command was used
        """
        try:
            with open(relative.make_relative("data/version"), "r", encoding="utf-8") as versionfile:
                currentVersion = versionfile.read()
        except Exception as err:
            logging.error("Failed to load version!")
            
        await ctx.send("Current commit#: "+currentVersion)