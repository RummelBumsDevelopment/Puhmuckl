# Echo: Responds with the args
from email.message import Message
from discord.ext import commands
from discord.message import Message
import time
class Ingmar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self,message:Message):
        if(not message.author.bot):
            if("schade um den punkt" in message.content.lower()):
                await message.channel.send("https://tenor.com/view/south-park-cartman-poop-homework-gif-12698863",delete_after=5)
                return
            if("卍" in message.content):
                await message.delete()


    @commands.command(name="ingmar", help="Ingmars")
    async def echo(self, ctx):
        await ctx.send("<:GetIngmart:929757284148600944>")