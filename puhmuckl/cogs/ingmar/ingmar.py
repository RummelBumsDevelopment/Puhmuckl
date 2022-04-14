# Echo: Responds with the args
from discord.ext import commands
from discord.message import Message
import time
from util import config

class Ingmar(commands.Cog):
    def __init__(self, bot:commands.bot.Bot):
        self.bot = bot

    test = commands

    @commands.Cog.listener()
    async def on_message(self,message:Message):
        if not message.author.bot:
            if "schade um den punkt" in message.content.lower():
                await message.channel.send("https://tenor.com/view/south-park-cartman-poop-homework-gif-12698863",delete_after=5)
                return
            if("卍" in message.content):
                await message.delete()
            
            if (("Ingmar" in message.content or "ingmar" in message.content) and message.content[0] is not config.get_client_config("prefix")):
                if not self.isIngmarAllowed(str(message.channel)):
                    await message.delete()
                    await message.channel.send("Halt dein Maul du Bastard!")


    @commands.group(pass_context=True)
    async def ingmar(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("<:GetIngmart:929757284148600944>")

    @ingmar.group(pass_context=True)
    async def allow(self, ctx):
        try:
            config.set_ingmar_allowedChannels(ctx.channel)
            await ctx.send("Ingmar ist ab hier zulässig")
        except FileExistsError:
            await ctx.send("Channel bereits erlaubt")
            return

    def isIngmarAllowed(self, currentChannel):
        # Returns true only if Ingmar is allowed to be mentioned here

        allowedChannels = config.get_ingmar_allowedChannels()

        for channel in allowedChannels:
            if channel == currentChannel:
                return True
        return False