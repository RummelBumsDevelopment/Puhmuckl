"""
Implements the Color Module
This is supposed to allow users to create own color roles, based on their hex-input.
"""

from email.message import Message
from discord.ext import commands
from discord import User
from discord import utils
class Color(commands.Cog):

    """Color cog"""
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="color", aliases=["colour"], help="Choose user color: <>color #FFFFFF")
    async def color(self, ctx: commands.context, *args):
        """Color command implementation

        Args:
            ctx (commands.context): Context in which the command was used
        """

        #First hex declaration
        hex = args[0]
        hex = hex.upper()

        # Remove preceding '#'
        if hex[0] == '#':
            hex = hex[1:]

        #Confirm if it COULD be converted to hex
        try:
            int(hex, 16)
        except Exception as e:
            await ctx.send("Bastard, das war falsch. Ich ficke dein Leben.")
            return

        #Check if hex is in allowed range
        if int(hex, 16) < 0 or int(hex, 16) > int("FFFFFF", 16):
            await ctx.send("Nur zwischen 0 und FFFFFF erlaubt. Was ist nur los mit dir <:sadge:902675012912300052>")
            return

        #Append Zeros until correct String size is reached
        while len(hex) < 6:
            hex = hex + '0'

        #convert hex to rgb
        rolename = name="#-"+hex
        hex = int(hex, 16)

        #remove existing color role
        userroles = ctx.message.author.roles
        for role in userroles:
            if role.name[0:2] == "#-":
                await ctx.message.author.remove_roles(role)
        
        
        #Get list of existing roles
        serverroles = ctx.guild.roles

        #Check if role for desired color already exists, and assign if it does
        if utils.get(ctx.guild.roles, name=rolename) is not None:
            await ctx.message.author.add_roles(utils.get(ctx.guild.roles, name=rolename))
            return

        #Create new role and assign it
        await ctx.guild.create_role(name=rolename,color=hex)
        await ctx.message.author.add_roles(utils.get(ctx.guild.roles, name=rolename))

        #Delete all empty color roles
        for roles in ctx.guild.roles:
            if roles.name[0:2] == "#-" and len(roles.members) == 0:
                print("Attemtping to delete: "+roles.name)
                await roles.delete()





