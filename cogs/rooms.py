from discord.ext import commands
from .embeds.rooms_embed import *
from .views.rooms_views import *
from discord.ext.commands import Context
from discord import File, app_commands


class Rooms(commands.Cog, name="rooms"):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.guild = None
        self.entry_room = None
        self.category = None

    @commands.Cog.listener()
    async def on_ready(self):
        self.guild = self.bot.get_guild(self.bot.config["GUILD_ID"])
        self.entry_room = self.bot.get_channel(self.bot.config["ENTRY_ROOM_CHANNEL_ID"])
        self.category = [
            *filter(
                lambda category: category.id == self.bot.config["ACTIVE_NOW_CATEGORY_ID"],
                self.guild.categories,
            )
        ][0]

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        # Check if user has joined entry room
        if before.channel != self.entry_room and after.channel == self.entry_room:
            has_room = await self.bot.database.is_owner(member.id)
            if not has_room:
                room_name = f"{member.name}'s room"
                user_room = await self.guild.create_voice_channel(
                    room_name, category=self.category, user_limit=5
                )
                await self.bot.database.add_user_room(member.id, user_room.id, room_name)
                await member.edit(voice_channel=user_room)
                invite_link = await user_room.create_invite(unique=True)
                await member.send(embed=get_room_link_embed(invite_link.url))
                return
            else:
                user_room_id = await self.bot.database.get_user_room_id(member.id)
                room = self.bot.get_channel(user_room_id)
                await member.edit(voice_channel=room)
                return

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        user_room_id = await self.bot.database.get_user_room_id(member.id)
        user_room = self.bot.get_channel(user_room_id)
        await self.bot.database.delete_user_room(member.id)
        if user_room:
            await user_room.delete()

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        is_user_channel = await self.bot.database.is_user_channel(channel.id)
        if is_user_channel:
            await self.bot.database.delete_user_room(room_id=channel.id)
        return

    @app_commands.command(
        name="panel_room_settings",
        description="Cоздать панель с настройками для личной комнаты.",
    )
    async def _panel_room_settings(self, context: Context) -> None:
        await context.interaction.response.defer(ephemeral=True)
        self.bot.logger.info(type(context))
        await context.reply("Создание панели...", ephemeral=True)
        await context.reply(file=File("src/banners/room_settings.png"))
        await context.reply(
            embed=get_room_settings_embed(), view=RoomSettingsView(self.bot.database)
        )

    async def setup_hook(self) -> None:
        self.add_view(RoomSettingsView(self.bot.database))


async def setup(bot) -> None:
    await bot.add_cog(Rooms(bot))
