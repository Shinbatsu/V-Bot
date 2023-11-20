from discord.ext import commands
from discord import ui, PartialEmoji, ButtonStyle, PermissionOverwrite
from discord.ui import View, button, Button
from discord.utils import get
from .embeds.navigation_embed import *
from discord import PermissionOverwrite


class NavigationView(
    View,
):
    def __init__(self, bot, rank_room_url, roles_room_url, settinigs_room_url):
        super().__init__()
        self.bot = bot
        roles_link = Button(label="⠀⠀Роли⠀⠀", style=ButtonStyle.url, url=roles_room_url)
        rank_link = Button(label="⠀Профиль", style=ButtonStyle.url, url=rank_room_url)
        settings_link = Button(label="Настройки", style=ButtonStyle.url, url=settinigs_room_url)
        self.add_item(roles_link)
        self.add_item(rank_link)
        self.add_item(settings_link)


# Here we name the cog and create a new class for the cog.
class Navigator(commands.Cog, name="navigator"):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.guild = None
        self.rank_room_url = None
        self.roles_room_url = None

    @commands.Cog.listener()
    async def on_ready(self):
        self.guild = self.bot.get_guild(self.bot.config["GUILD_ID"])

        self.rank_room = self.bot.get_channel(self.bot.config["RANK_ROOM_CHANNEL_ID"])
        invite_link = await self.rank_room.create_invite(unique=True)
        self.rank_room_url = invite_link.url

        self.roles_room = self.bot.get_channel(self.bot.config["ROLES_ROOM_CHANNEL_ID"])
        invite_link = await self.roles_room.create_invite(unique=True)
        self.roles_room_url = invite_link.url

        self.settings_room = self.bot.get_channel(self.bot.config["ROOM_SETTINGS_CHANNEL_ID"])
        invite_link = await self.settings_room.create_invite(unique=True)
        self.settings_room_url = invite_link.url

    @commands.hybrid_command(
        name="panel_navigation",
        with_app_command=True,
        description="Cоздать панель с навигационными кнопками.",
    )
    @commands.has_role("Администратор")
    async def panel_navigation(self, ctx):
        await ctx.defer()
        await ctx.message.delete()
        if ctx.channel.id != self.bot.config["NAVIGATION_CHANNEL_ID"]:
            return
        await ctx.send(navigation_banner)
        await ctx.send(
            embed=get_navigation_room_embed(self.bot),
            view=NavigationView(
                self.bot, self.rank_room_url, self.roles_room_url, self.settings_room_url
            ),
        )


# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot) -> None:
    await bot.add_cog(Navigator(bot))
