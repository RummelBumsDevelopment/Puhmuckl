# Echo: Responds with the args
from discord.ext import commands
from discord.message import Message
import time
import logging
from util import config

# Zensursula actively deletes unwanted text and responds to specific keywords

class Zensursula(commands.Cog):
    def __init__(self, bot:commands.bot.Bot):
        self.bot = bot

    @commands.Cog.listener()
    # This contains the hardcoded responses and Censorship
    async def on_message(self,message:Message):
        if not message.author.bot:

            logging.info("|"+str(message.channel)+"| "+str(message.author)+": "+str(message.content))
            
            if "schade um den punkt" in message.content.lower():
                await message.channel.send("https://tenor.com/view/south-park-cartman-poop-homework-gif-12698863",delete_after=5)
                return
            if("卍" in message.content):
                await message.delete()
            
            # Censorship
            if (self.isChannelCensored(message.channel) and self.checkForCensoredWord(message.content)):
                await message.channel.send("Halt dein Maul du Bastard!")
                await message.delete()
                

    @commands.group(pass_context=True, aliases=["zensur"])
    async def zensursula(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Kommando unvollständig! Krieg mal dein Leben in den Griff...")


    @zensursula.group(pass_context=True, help="Disable Censorship in current channel")
    async def disable(self, ctx):
        try:
            config.set_channelCensorship(ctx.channel, False)
            await ctx.send("Dieser Kanal wird ab sofort nicht weiter Zensiert.")
        except FileExistsError:
            await ctx.send("Fick dich, der ist schon unzensiert. Erst nachdenken dann schreiben.")
            return


    @zensursula.group(pass_context=True, help="Enable censorship in current channel")
    async def enable(self, ctx):
        try:
            config.set_channelCensorship(ctx.channel, True)
        except FileExistsError:
            await ctx.send("Der Channel wird überhaupt nicht zensiert du Opfer.")
            return
        await ctx.send("Channel ist zensiert. Das gilt ab sofort, unverzüglich.")


    @zensursula.group(pass_context=True, help="Enable censorship in current channel")
    async def list(self, ctx):
            
        await ctx.send("Unzensierte Channel: "+str(config.get_uncensoredChannels()))


    def isChannelCensored(self, currentChannel):
        # Returns true only if channel is beeing censored

        allowedChannels = config.get_uncensoredChannels()

        for channel in allowedChannels:
            if channel == str(currentChannel):
                logging.debug("Channel is not censored!")
                return False
        logging.debug("Channel is beeing censored!")
        return True


    def checkForCensoredWord(self, content):
        # Checks if provided String contains censored words, returns False if not

        censoredWords = config.get_censoredWords()

        for word in censoredWords:
            if word.lower() in str(content).lower():
                return True
        return False