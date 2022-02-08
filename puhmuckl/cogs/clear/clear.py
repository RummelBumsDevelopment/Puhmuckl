"""
Implements the Clear module
"""
from ast import arg
from discord.ext import commands
class Clear(commands.Cog):

    """Clear cog"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="clear",help = "clears the whole channel needs confirm of 3") 
    async def clear(self,ctx:commands.context):
        """clear command implementation

        Args:
            ctx (commands.context): Context in which the command was used

        checks if channel to be cleared has bot-dev role as a security

        """
        for role in ctx.channel.changed_roles:
            if role.name == "bot-dev":
                poll = await ctx.send("are you sure you want to clear the whole channel?")
                await poll.add_reaction("<:pepeyes:902675012555771914>")
                return
        await ctx.send("clear not allowed in this channel")

    """Reaction listener
    """
    @commands.Cog.listener()
    async def on_reaction_add(self,reaction):

        """
            clear handler
            
            checks if reaction was added to message sent by bot
            checks count of reactions with specific emote
            
            removes messages from chat
        """
        if reaction.message.content == "are you sure you want to clear the whole channel?":
            if reaction.message.author.id == self.bot.user.id:
                if str(reaction.emoji) == "<:pepeyes:902675012555771914>":
                    if reaction.count >=4:
                        await reaction.message.channel.send("channel will be cleared takes a while")
                        await reaction.message.channel.purge()
                        await reaction.message.channel.send("Welcome to your new empty channel")
