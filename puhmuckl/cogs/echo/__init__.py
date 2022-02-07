"""
Includes the Echo module
"""
from .echo import Echo

"""
Sets up the bot (adds the cog)
"""
def setup(bot):
    bot.add_cog(Echo(bot))
