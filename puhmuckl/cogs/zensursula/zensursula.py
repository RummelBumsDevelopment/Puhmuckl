# Echo: Responds with the args
import discord
from discord.ext import commands
from discord.message import Message
import logging, random, re
from util import config


class Zensursula(commands.Cog):
    '''Zensursula actively deletes unwanted text and responds to specific keywords'''
    
    censorship_history = {}
    
    def __init__(self, bot:commands.bot.Bot):
        self.logger = logging.getLogger("puhmuckl.zensursula")
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self,message:Message):
        '''This function combined with its decorator reacts to written messages.'''
        
        if not message.author.bot:
            self.logger.info("|"+str(message.channel)+"| "+str(message.author)+": "+str(message.content))
            
            # censorship first
            if (self.isChannelCensored(message.channel) and self.checkForCensoredWord(message.content)):
                self.censorship_history[message.channel.id] = {
                    "name" : message.author.nick,
                    "image" : message.author.display_avatar,
                    "content" : self.replace_censored(message.content),
                }
                
                await message.channel.send(self.get_insult(message.author.nick))
                await message.delete()
                return
            
            # Other reactions to specific keywords
            msg_lower = message.content.lower()

            if "schade um den punkt" in msg_lower:
                await message.channel.send("https://tenor.com/view/south-park-cartman-poop-homework-gif-12698863",delete_after=5)
            

    @commands.group(pass_context=True, aliases=["zensur"])
    async def zensursula(self, ctx):
        '''Base command, does nothing.'''
        if ctx.invoked_subcommand is None:
            await ctx.send("Kommando unvollständig! Krieg mal dein Leben in den Griff...")


    @zensursula.group(pass_context=True, help="Disable Censorship in current channel")
    async def disable(self, ctx):
        try:
            self.set_channelCensorship(ctx.channel, False)
            await ctx.send("Dieser Kanal wird ab sofort nicht weiter Zensiert.")
        except FileExistsError:
            await ctx.send("Fick dich, der ist schon unzensiert. Erst nachdenken dann schreiben.")
            return


    @zensursula.group(pass_context=True, help="Enable censorship in current channel")
    async def enable(self, ctx):
        try:
            self.set_channelCensorship(ctx.channel, True)
        except FileExistsError:
            await ctx.send("Der Channel wird überhaupt nicht zensiert du Opfer.")
            return
        await ctx.send("Channel ist zensiert. Das gilt ab sofort, unverzüglich.")


    @zensursula.group(pass_context=True, help="Returns list of censored channels")
    async def list(self, ctx):
        #TODO Maybe make it independend of the server
        await ctx.send("Unzensierte Channel: "+str(self.get_uncensoredChannels()))


    @zensursula.group(pass_context=True, help="Restores latest deleted message.")
    async def restore(self, ctx):
        '''This function will restore the latest deleted message in the current channel (stored in dict within this class)'''

        if ctx.message.channel.id in self.censorship_history:
            if self.censorship_history[ctx.message.channel.id] is not None:
                old_message = self.censorship_history[ctx.message.channel.id]
                
                msg_embed = {
                    "author":{
                        "name": str(old_message["name"]),
                        "icon_url": str(old_message["image"])
                        },
                    "description": str(old_message["content"])
                    }
                await ctx.send(embed=discord.Embed.from_dict(msg_embed))
                
                # clear history
                self.censorship_history[ctx.message.channel.id] = None            
            else:
                await ctx.send("Nichts gefunden. Verpiss dich.")


    def isChannelCensored(self, currentChannel):
        '''Returns true only if channel is beeing censored'''

        allowedChannels = self.get_uncensoredChannels()

        for channel in allowedChannels:
            if channel == str(currentChannel):
                self.logger.debug("Channel is not censored!")
                return False
        self.logger.debug("Channel is beeing censored!")
        return True


    def checkForCensoredWord(self, content):
        '''Checks if provided String contains censored words, returns False if not'''

        censoredWords = config.get_config("ZENSURSULA","censoredwords").split(",")

        for word in censoredWords:
            if word.lower() in str(content).lower():
                return True
        return False


    def get_uncensoredChannels(self):
        '''Returns list of uncensored channels'''
        return config.get_config("ZENSURSULA","uncensoredchannels").split(",")


    def add_uncensoredChannel(self, newChannel):
        # Writes channel list into .ini 
        uncensoredchannels = config.get_config("ZENSURSULA","uncensoredchannels").split(",")
        uncensoredchannels.append(newChannel)
        config.set_config("ZENSURSULA","uncensoredchannels", ",".join(uncensoredchannels))


    def set_channelCensorship(self, newChannel, censorship):
        # Adds new Channel to list of allowed channels

        # pull list of currently uncensored channels
        uncensoredChannels = config.get_config("ZENSURSULA","uncensoredChannels").split(",")

        if censorship:
            # channel will be censored
            if str(newChannel) in uncensoredChannels:
                uncensoredChannels.remove(str(newChannel))
            else:
                raise FileExistsError
        else:
            # channel will be uncensored
            if str(newChannel) in uncensoredChannels:
                raise FileExistsError
            uncensoredChannels.append(str(newChannel))

        # clean up empty lines (If there are any)
        try:
            uncensoredChannels.remove("")
        except ValueError:
            # continue if empty string is not present
            pass

        # Make list string again and set config
        config.set_config("ZENSURSULA","uncensoredChannels",",".join(uncensoredChannels))
        return
    

    def get_insult(self, name) -> str:
        '''Returns insult from list in function.'''
        insults = [
            f"{name}, halt dein Maul du Bastard.",
            f"{name} ist ein Hurensohn.",
            f"Wallah Krise, sag doch nicht sowas {name}",
            f"{name} macht einfach diesen <:sadge:902675012912300052>",
            f"Wenn {name} sein Nachricht ist sus <:amogus:1035576042779316276>",
            f"{name} schafft es nicht das Maul zu halten.",
            f"{name} rafft nicht wann Schluss ist",
            f"Der kleine {name} steht and der Info und sucht seinen Betreuer."
        ]

        if not "i" in name:
            insults.append(f"Das 'i' in {name} steht für intelligent.")

        return random.choice(insults)

    
    def replace_censored(self, message: str) -> str:
        '''Takes string and replaces censored words with **ZENSIERT**'''
        censoredWords = config.get_config("ZENSURSULA","censoredwords").split(",")

        result = message

        for word in censoredWords:
            pattern = re.compile(re.escape(word), re.IGNORECASE)
            result = pattern.sub("**ZENSIERT**", result)
        return result



if __name__ == "__main__":
    logging.error("This file is not supposed to be executed.")