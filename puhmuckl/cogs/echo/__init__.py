"""
Includes the Echo module
"""
from .echo import Echo

def setup(bot):
    """Sets up the bot (adds the cog)

    Args:
        bot (discord.bot): Bot to which to add the cog
    """
    bot.add_cog(Echo(bot))
