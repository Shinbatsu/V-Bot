from discord import TextStyle
from discord.ui import TextInput, Modal, button
from ..embeds.roles_embed import *
import discord
from bs4 import BeautifulSoup
import aiohttp
import re


async def fetch_rank(nickname):
    name = nickname.split("#")[0]
    subname = nickname.split("#")[1]
    url = f"https://tracker.gg/valorant/profile/riot/{name}%23{subname}/overview"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response = await response.text()

            soup = BeautifulSoup(response, "html.parser")
            items = soup.find_all("div", class_="rating-entry__rank-info")

            for i in items:
                out = i.find("div", class_="value").text
                return re.sub("[\W\d]+", "", out)
            return None


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
        riot_username = str(self.rank.value)
        riot_username_repeat = str(self.rank_check.value)
        if riot_username != riot_username_repeat:
            await interaction.response.send_message(
                embed=get_different_nicknames_embed(self.bot, riot_username, riot_username_repeat)
            )
        else:
            already_has_nickname = bool(
                await self.bot.database.get_valorant_nickname(user_id=interaction.user.id)
            )
            if already_has_nickname:
                who_has_this_nick_id = await self.bot.database.get_user_id_by_nickname(
                    nickname=riot_username
                )
                user = self.bot.get_user(int(who_has_this_nick_id))
                await interaction.response.send_message(
                    embed=get_already_has_nickname_embed(self.bot, user.name)
                )
            else:
                rank = await fetch_rank(self.rank.value)
                if rank:
                    username = interaction.user.name
                    await self.bot.database.updata_nick_name(
                        user_id=interaction.user.id, valorant_nickname=riot_username
                    )
                    await interaction.user.add_roles(
                        discord.utils.get(interaction.user.guild.roles, name=rank)
                    )
                    await interaction.response.send_message(
                        embed=get_you_got_rank_embed(self.bot, username=username, rank=rank),
                        ephemeral=True,
                    )
                else:
                    await interaction.response.send_message(
                        embed=get_cant_get_rank_embed(self.bot), ephemeral=True
                    )
