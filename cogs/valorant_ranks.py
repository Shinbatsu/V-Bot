from discord.ext import commands
from discord.ext.commands import Context
from discord import Embed, ui, PartialEmoji, TextStyle, Colour, ButtonStyle
from discord.interactions import Interaction
from discord.ui import View, TextInput, Modal, button

from .embeds.valorant_ranks_embed import *
import discord
from bs4 import BeautifulSoup
import aiohttp
import re


async def fetch_rank(nickname):
    name = nickname.split("#")[0]
    digits = nickname.split("#")[1]
    url = f"https://tracker.gg/valorant/profile/riot/{name}%23{digits}/overview"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response = await response.text()

            soup = BeautifulSoup(response, "html.parser")
            items = soup.find_all("div", class_="rating-entry__rank-info")

            for i in items:
                out = i.find("div", class_="value").text
                return re.sub("[\W\d]+", "", out)
            return None


# Here we name the cog and create a new class for the cog.
class UserValorant(commands.Cog, name="user_valorant"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command()
    async def pick_rank(self, ctx):
        if ctx.channel.id != self.bot.config["ROLES_ROOM_CHANNEL_ID"]:
            return
        await ctx.send(valorant_ranking_banner)
        await ctx.send(embed=get_pick_rank_embed(self.bot), view=UserRoleView(self.bot))


class RankModal(Modal, title="RIOT ник"):
    rank = TextInput(
        label="Введите имя игрока",
        placeholder="User#0000",
        style=TextStyle.short,
        required=True,
        max_length=30,
    )
    rank_check = TextInput(
        label="Повторите имя игрока",
        placeholder="User#0000",
        style=TextStyle.short,
        required=True,
        max_length=30,
    )

    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    async def on_submit(self, interaction) -> None:
        riot_user_name = str(self.rank.value)
        riot_user_name_repeat = str(self.rank_check.value)
        if riot_user_name != riot_user_name_repeat:
            await interaction.response.send_message(
                embed=get_different_nicknames_embed(self.bot, riot_user_name, riot_user_name_repeat)
            )
        else:
            already_has_nickname = bool(
                await self.bot.database.get_valorant_nickname(user_id=interaction.user.id)
            )
            if already_has_nickname:
                who_has_this_nick_id = await self.bot.database.get_user_id_by_nickname(
                    nickname=riot_user_name
                )
                user = self.bot.get_user(int(who_has_this_nick_id))
                await interaction.response.send_message(
                    embed=get_already_has_nickname_embed(self.bot, user.name)
                )
            else:
                rank = await fetch_rank(self.rank.value)
                if rank:
                    user_name = interaction.user.name
                    await self.bot.database.updata_nick_name(
                        user_id=interaction.user.id, valorant_nickname=riot_user_name
                    )
                    await interaction.user.add_roles(
                        discord.utils.get(interaction.user.guild.roles, name=rank)
                    )
                    await interaction.response.send_message(
                        embed=get_you_got_rank_embed(self.bot, user_name=user_name, rank=rank),
                        ephemeral=True,
                    )
                else:
                    await interaction.response.send_message(
                        embed=get_cant_get_rank_embed(self.bot), ephemeral=True
                    )


class UserRoleView(View):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    @button(label="⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀GET RANK⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀", row=1, style=ButtonStyle.success)
    async def get_rank(self, interaction, button):
        await interaction.response.send_modal(RankModal(self.bot))


# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot) -> None:
    await bot.add_cog(UserValorant(bot))
