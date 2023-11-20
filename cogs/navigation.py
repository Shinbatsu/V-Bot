from discord.ext import commands
from .embeds.navigation_embed import *
from discord.ext.commands import Context

# from .views.navigation_views import *
from discord import File

from discord import ButtonStyle
from discord.ui import View, Button


class NavigationView(
    View,
):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        roles_link = Button(
            label="⠀⠀Роли⠀⠀",
            style=ButtonStyle.url,
            url="https://discord.com/channels/711201809372414062/1174660820991475712",
        )
        rank_link = Button(
            label="⠀Профиль",
            style=ButtonStyle.url,
            url="https://discord.com/channels/711201809372414062/1174660701076344852",
        )
        settings_link = Button(
            label="Настройки",
            style=ButtonStyle.url,
            url="https://discord.com/channels/711201809372414062/1171723459039088740",
        )
        self.add_item(roles_link)
        self.add_item(rank_link)
        self.add_item(settings_link)


# Here we name the cog and create a new class for the cog.
class Navigation(commands.Cog, name="navigation"):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.guild = None
        self.rank_room_url = None
        self.roles_room_url = None
        self.settings_room_url = None

    async def on_ready(self):
        self.guild = self.bot.get_guild(self.bot.config["GUILD_ID"])
        self.rank_room = self.bot.get_channel(self.bot.config["RANK_ROOM_CHANNEL_ID"])
        invite_link = await self.rank_room.create_invite(unique=True)
        self.rank_room_url = "https://discord.com/channels/711201809372414062/1174660701076344852"
        self.roles_room = self.bot.get_channel(self.bot.config["ROLES_ROOM_CHANNEL_ID"])
        invite_link = await self.roles_room.create_invite(unique=True)
        self.roles_room_url = "https://discord.com/channels/711201809372414062/1174660820991475712"
        self.settings_room = self.bot.get_channel(self.bot.config["ROOM_SETTINGS_CHANNEL_ID"])
        invite_link = await self.settings_room.create_invite(unique=True)
        self.settings_room_url = (
            "https://discord.com/channels/711201809372414062/1171723459039088740"
        )

    @commands.hybrid_command(
        name="panel_navigation",
        description="Cоздать панель с навигационными кнопками.",
    )
    @commands.has_role("Администратор")
    async def panel_navigation(self, ctx: Context) -> None:
        await ctx.send(file=File("src/banners/navigation.png"))
        await ctx.send(
            embed=get_navigation_room_embed(self.bot),
            view=NavigationView(self.bot),
        )


# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot) -> None:
    await bot.add_cog(Navigation(bot))
