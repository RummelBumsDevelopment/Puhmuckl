'''
This is the cog that allows users to
fetch an AI-generated inspirational quote
made by Inspirobot
'''
import discord

from discord.ext import commands
import requests

class Inspire(commands.Cog):

	def get_inspirational_quote() -> str:
		response = requests.get("http://inspirobot.me/api?generate=true")

		if not response.ok:
			logging.error(f"Inspirobot API response not OK: {response.status_code} [http://inspirobot.me/api?generate=true]")
			return None

		return response.text

	def __init__(self, client : discord.Client):
		self.client = client

	@commands.command(name="inspire", description="Sends a randomly generated inspirational quote", usage="inspire", aliases=["insp"])
	@commands.cooldown(1, 5)
	async def inspire(self, ctx : commands.Context):
		image = Inspire.get_inspirational_quote()
		if image is None:
			await ctx.message.add_reaction("⚠️")
		else:
			embed = discord.Embed(title="Inspirational Quote", color=0x2596be)
			embed.set_image(url=image)
			await ctx.send(embed=embed)
