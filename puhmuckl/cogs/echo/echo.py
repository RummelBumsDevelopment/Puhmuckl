"""
Implements the Echo module
"""
from discord.ext import commands

"""
Echo cog
"""
class Echo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """
    The echo commands simply echoes back what the user supplies as args
    """
    @commands.command(name="echo", help="Echos the user args")
    async def echo(self, ctx, *args):
        await ctx.send(" ".join(args))
