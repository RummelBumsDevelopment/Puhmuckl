"""
Includes the Echo module
"""
from .clear import Clear

def setup(bot):
    """Sets up the bot (adds the cog)
    Args:
        bot (discord.bot): Bot to which to add the cog
    """
    bot.add_cog(Clear(bot))