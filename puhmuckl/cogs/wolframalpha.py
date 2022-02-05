import discord
from discord.ext import commands
from util import interactive

class TestEmbed(interactive.InteractiveEmbed):
    REACTIONS = {
        "close": "❌"
    }

    def __init__(self, parent, ctx):
        super(TestEmbed, self).__init__(parent.bot, ctx, 60.0)
        self.parent = parent
        self.owner = self.ctx.author

    async def add_navigation(self, message):
        await message.add_reaction(TestEmbed.REACTIONS["close"])

    async def on_reaction(self, reaction, user):
        if reaction.emoji == TestEmbed.REACTIONS["close"]:
            await self.close_embed()

    async def on_close(self):
        self.parent.activeObjects.pop(self.ctx.channel.id)

    def make_embed(self):
        embed = discord.Embed(
            title = "Wolfram|Alpha Test",
            description = "This is a test embed. You can close it by reacting with ❌",
            color = 0xff7e00
        )

        return embed

class WolframAlpha(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        self.activeObjects = {}

    @commands.command(name="wolframalpha", description="Queries Wolfram|Alpha", usage="<query>", aliases=["wolf", "wa"])
    async def wolframalpha(self, ctx, *query):
        self.activeObjects[ctx.channel.id] = TestEmbed(self, ctx)
        await self.activeObjects[ctx.channel.id].show_embed()

def setup(bot: commands.Bot):
    bot.add_cog(WolframAlpha(bot))