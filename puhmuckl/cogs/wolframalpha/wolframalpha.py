from pydoc import describe
import discord, logging
from discord.ext import commands
from cogs.wolframalpha.wolframapi import WolframDidYouMean, WolframResponse
from util import interactive

WOLFRAM_COLOR = 0xff7e00

class WolframDidYouMeanEmbed(interactive.InteractiveEmbed):
    REACTIONS = {
        "close": "❌",
        "accept": "✅",
        "next": "➡️",
        "previous": "⬅️"
    }

    def __init__(self, parent, ctx, response: WolframResponse):
        super(WolframDidYouMeanEmbed, self).__init__(parent.bot, ctx, 60.0)
        self.parent = parent
        self.owner = self.ctx.author

        self.response = response
        self.selection = 0

    async def add_navigation(self, message):
        await message.add_reaction(WolframDidYouMeanEmbed.REACTIONS["close"])
        await message.add_reaction(WolframDidYouMeanEmbed.REACTIONS["accept"])

        if len(self.response.did_you_means) > 1:
            await message.add_reaction(WolframDidYouMeanEmbed.REACTIONS["previous"])
            await message.add_reaction(WolframDidYouMeanEmbed.REACTIONS["next"])


    async def on_reaction(self, reaction, user):
        if reaction.emoji == WolframDidYouMeanEmbed.REACTIONS["close"]:
            await self.close_embed()

        if reaction.emoji == WolframDidYouMeanEmbed.REACTIONS["accept"]:
            await self.close_embed()
            await self.message.delete()
            await self.parent.query(self.ctx, self.response.did_you_means[self.selection].content)

        if reaction.emoji == WolframDidYouMeanEmbed.REACTIONS["next"]:
            self.selection += 1
            if self.selection >= len(self.response.did_you_means):
                self.selection = 0

            await reaction.remove(user)

        if reaction.emoji == WolframDidYouMeanEmbed.REACTIONS["previous"]:
            self.selection -= 1
            if self.selection < 0:
                self.selection = len(self.response.did_you_means) - 1  

            await reaction.remove(user) 

    def make_embed(self):
        did_you_mean = self.response.did_you_means[self.selection].content

        embed = discord.Embed(
            title = "Did you mean...",
            description = did_you_mean,
            color = WOLFRAM_COLOR
        )

        if len(self.response.did_you_means) > 1:
            footer_text = f"Entry {self.selection + 1}/{len(self.response.did_you_means)}"
            embed.set_footer(text = footer_text)

        return embed


class WolframEmbed(interactive.InteractiveEmbed):
    REACTIONS = {
        "close": "❌",
        "next": "⬇️",
        "previous": "⬆️"
    }

    def __init__(self, parent, ctx, response: WolframResponse):
        super(WolframEmbed, self).__init__(parent.bot, ctx, 60.0)
        self.parent = parent
        self.owner = self.ctx.author

        self.response = response
        self.selected_pod = 0

        if "input" in self.response.pods[0].title.lower():
            self.selected_pod = 1

    async def add_navigation(self, message):
        await message.add_reaction(WolframEmbed.REACTIONS["close"])
        await message.add_reaction(WolframEmbed.REACTIONS["previous"])
        await message.add_reaction(WolframEmbed.REACTIONS["next"])

    async def on_reaction(self, reaction, user):
        if reaction.emoji == WolframEmbed.REACTIONS["close"]:
            await self.close_embed()

        if reaction.emoji == WolframEmbed.REACTIONS["next"]:
            self.selected_pod += 1
            if self.selected_pod >= self.response.numpods:
                self.selected_pod = 0

            await reaction.remove(user)

        if reaction.emoji == WolframEmbed.REACTIONS["previous"]:
            self.selected_pod -= 1
            if self.selected_pod < 0:
                self.selected_pod = self.response.numpods - 1  

            await reaction.remove(user)  

    def make_embed(self):
        pod = self.response.pods[self.selected_pod]
        title = pod.title

        embed = discord.Embed(
            title = title,
            color = WOLFRAM_COLOR
        )

        embed.set_image(url = pod.subpods[0].image.src)

        footer_text = f"Pod {self.selected_pod + 1}/{self.response.numpods}"
        embed.set_footer(text = footer_text)

        return embed

class WolframAlpha(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def query(self, ctx: commands.Context, query: str):
        if query is None:
            embed = discord.Embed(
                title = "Error",
                description = "Please supply a query",
                color = WOLFRAM_COLOR
            )

            await ctx.send(embed = embed)
            return

        embed = discord.Embed(
            title = "Querying Wolfram|Alpha...",
            description = "This can take up to 45 seconds",
            color = WOLFRAM_COLOR
        )
        loading_embed = await ctx.send(embed = embed)

        response = WolframResponse(query)
        await loading_embed.delete()

        if not response.success:
            if len(response.did_you_means) == 0:
                embed = discord.Embed(
                    title = "Error",
                    description = response.error,
                    color = WOLFRAM_COLOR
                )
                await ctx.send(embed = embed)

            else:
                await WolframDidYouMeanEmbed(self, ctx, response).show_embed()
            
            return

        await WolframEmbed(self, ctx, response).show_embed()

    @commands.command(name="wolframalpha", description="Queries Wolfram|Alpha", usage="<query>", aliases=["wolf", "wa"])
    async def wolframalpha(self, ctx: commands.Context, *,  query):
        logging.debug(query)
        await self.query(ctx, query)
