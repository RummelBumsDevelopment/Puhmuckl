"""
Implements the Echo module
"""
from ast import arg
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
        if "-r" in args:
            await ctx.message.delete()
            await ctx.send(" ".join(x for x in args if x != "-r"))
            return
        await ctx.send(" ".join(args))
