"""
Includes the inspire module
"""
from .inspire import Inspire

def setup(bot):
	"""Sets up the bot (adds the cog)

	Args:
		bot (discord.bot): Bot to which to add the cog
	"""
	bot.add_cog(Inspire(bot))