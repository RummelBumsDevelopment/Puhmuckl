from discord.ext import commands
import discord
from cogs.wolframalpha.wolframapi import WolframDidYouMean, WolframResponse
from cogs.skyblock.elections import ElectionRequest
import matplotlib.pyplot as plt

class Skyblock(commands.Cog):
    COLORS = {
        "error": 0xba0101,
        "default": 0x13c7f4
    }

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.group(name="skyblock", description="Group for Hypixel Skyblock related commands", aliases=["sb"], invoked_subcommand=True)
    async def skyblock(self, ctx):
        pass

    @skyblock.command(name="mayor", description="Outputs the current mayor")
    async def mayor(self, ctx):
        request = ElectionRequest()

        if request.success is None:
            embed = discord.Embed(
                title = "Request to Hypixel API failed",
                color = Skyblock.COLORS["error"]
            )
            await ctx.send(embed=embed)
            return

        mayor = request.mayor
        embed = discord.Embed(
            title = mayor.name,
            description = mayor.key,
            color = Skyblock.COLORS["default"]
        )

        for perk in mayor.perks:
            embed.add_field(
                name = perk.name,
                value = perk.description
            )

        await ctx.send(embed=embed)

    @skyblock.command(name="election", description="Displays the results of the current elections")
    async def election(self, ctx):
        request = ElectionRequest()

        if request.success is None:
            embed = discord.Embed(
                title = "Request to Hypixel API failed",
                color = Skyblock.COLORS["error"]
            )
            await ctx.send(embed=embed)
            return

        if request.current_election is None:
            embed = discord.Embed(
                title = "There is no ongoing election",
                color = Skyblock.COLORS["default"]
            )
            await ctx.send(embed=embed)
            return

        data = []
        labels = []
        for candidate in request.current_election.candidates:
            data.append(candidate.votes)
            labels.append(f"{candidate.name} ({candidate.key})")

        plt.yticks(range(len(data)), labels)
        plt.ylabel("Candidates")
        plt.xlabel("Votes")
        plt.title(f"Election results (Year {request.current_election.year})")
        plt.barh(range(len(data)), data)
        plt.savefig("election.png", bbox_inches='tight',dpi=100)

        file = discord.File("election.png")
        embed = discord.Embed(
            title = "Current election",
            color = Skyblock.COLORS["default"]
        )
        embed.set_image(url = "attachment://election.png")
        embed.set_footer(text = f"Last updated: {request.last_updated.strftime('%d.%m.%Y at %H:%M:%S')}")

        await ctx.send(file = file, embed = embed)
