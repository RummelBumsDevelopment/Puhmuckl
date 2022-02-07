"""
Implements the Echo module
"""
from discord.ext import commands

class Echo(commands.Cog):
    """Echo cog"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="echo", help="Echos the user args")
    async def echo(self, ctx: commands.context, *args):
        """Echo command implementation

        Args:
            ctx (commands.context): Context in which the command was used
        """
        await ctx.send(" ".join(args))
