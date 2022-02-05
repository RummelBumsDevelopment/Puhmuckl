# Echo: Responds with the args
from discord.ext import commands

class Echo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="echo", help="Echos the user args")
    async def echo(self, ctx, *args):
        await ctx.send(" ".join(args))

def setup(bot):
    bot.add_cog(Echo(bot))