from discord.ext import commands
from discord import ui, PartialEmoji, ButtonStyle, PermissionOverwrite
from discord.ui import View, button
from discord.utils import get
from .embeds.self_rooms_embed import *
from .modals.self_rooms_modals import *
from discord import PermissionOverwrite


class SelfRooms(commands.Cog, name="self_rooms"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.guild = self.bot.get_guild(self.bot.config["GUILD_ID"])
        self.entry_room = get(
            self.guild.voice_channels, id=self.bot.config["ENTRY_ROOM_CHANNEL_ID"]
        )
        self.category = get(
            self.guild.categories,
            id=self.bot.config["ACTIVE_NOW_CATEGORY_ID"],
        )

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
                await member.send(embed=get_room_link_embed(self.bot, invite_link.url))
                return
            else:
                room_id = await self.bot.database.get_user_room_id(member.id)
                room = get(self.guild.channels, id=room_id)
                await member.edit(voice_channel=room)
                return

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        user_room_id = await self.bot.database.get_user_room_id(member.id)
        user_room = get(self.guild.voice_channels, id=user_room_id)
        await self.bot.database.delete_user_room(member.id)
        await user_room.delete()

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        is_user_channel = await self.bot.database.is_user_channel(channel.id)
        if is_user_channel:
            await self.bot.database.delete_user_room(room_id=channel.id)
        return

    @commands.command()
    @commands.has_role("Creator")
    async def room_settings_panel(self, ctx):
        if ctx.channel.id != self.bot.config["ROOM_SETTINGS_CHANNEL_ID"]:
            return
        await ctx.message.delete()
        await ctx.send(room_settings_banner)
        await ctx.send(embed=get_room_settings_embed(self.bot), view=RoomSettingsView(self.bot))


class RoomSettingsView(
    View,
):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.cooldown = commands.CooldownMapping.from_cooldown(1, 60, commands.BucketType.member)

    @button(
        label="",
        emoji=PartialEmoji.from_str("<:custom_lock:1173271460970758204>"),
        row=0,
        style=ButtonStyle.secondary,
    )
    async def lock(self, interaction, button):
        member = interaction.user
        is_owner = await self.bot.database.is_owner(interaction.user.id)
        if is_owner:
            is_closed = await self.bot.database.get_is_closed_room(user_id=interaction.user.id)
            user_room_id = await self.bot.database.get_user_room_id(interaction.user.id)
            guild = self.bot.get_guild(self.bot.config["GUILD_ID"])
            user_room = get(guild.voice_channels, id=user_room_id)
            if not is_closed:
                await user_room.edit(
                    overwrites={
                        member: PermissionOverwrite(connect=False),
                        guild.default_role: PermissionOverwrite(connect=False),
                    }
                )
                await interaction.response.send_message(
                    embed=get_room_closed_embed(self.bot), ephemeral=True
                )
                await self.bot.database.update_is_close_user_room(
                    room_id=user_room_id, is_close=True
                )
            else:
                await user_room.edit(
                    overwrites={
                        member: PermissionOverwrite(connect=True),
                        guild.default_role: PermissionOverwrite(connect=True),
                    }
                )
                await interaction.response.send_message(
                    embed=get_room_opened_embed(self.bot), ephemeral=True
                )
                await self.bot.database.update_is_close_user_room(
                    room_id=user_room_id, is_close=False
                )
        else:
            await interaction.response.send_message(
                embed=get_havent_room_embed(self.bot), ephemeral=True
            )

    @button(
        label="",
        emoji=PartialEmoji.from_str("<:kick:1173271463244087336>"),
        row=0,
        style=ButtonStyle.secondary,
    )
    async def kick(self, interaction, button):
        is_owner = await self.bot.database.is_owner(interaction.user.id)
        if is_owner:
            await interaction.response.send_modal(KickModal(self.bot))
            return
        else:
            await interaction.response.send_message(
                embed=get_havent_room_embed(self.bot), ephemeral=True
            )

    @button(
        label="",
        emoji=PartialEmoji.from_str("<:slots:1173271467060904050>"),
        row=0,
        style=ButtonStyle.secondary,
    )
    async def slots(self, interaction, button):
        is_owner = await self.bot.database.is_owner(interaction.user.id)
        if is_owner:
            await interaction.response.send_modal(ChangeSlotsModal(self.bot))
        else:
            await interaction.response.send_message(
                embed=get_havent_room_embed(self.bot), ephemeral=True
            )

    @button(
        label="",
        row=0,
        emoji=PartialEmoji.from_str("<:change_owner:1173271455786602526>"),
        style=ButtonStyle.secondary,
    )
    async def change_owner(self, interaction, button):
        is_owner = await self.bot.database.is_owner(interaction.user.id)
        if is_owner:
            await interaction.response.send_modal(ChangeOwnerModal(self.bot))
        else:
            await interaction.response.send_message(
                embed=get_havent_room_embed(self.bot), ephemeral=True
            )

    @button(
        label="",
        row=0,
        emoji=PartialEmoji.from_str("<:rename:1173271464699498677>"),
        style=ButtonStyle.secondary,
    )
    async def rename(self, interaction, button):
        is_owner = await self.bot.database.is_owner(interaction.user.id)
        if is_owner:
            await interaction.response.send_modal(RenameRoomModal(self.bot))
        else:
            await interaction.response.send_message(
                embed=get_havent_room_embed(self.bot), ephemeral=True
            )

    @button(label="⠀⠀⠀⠀⠀⠀⠀⠀CREATE ROOM⠀⠀⠀⠀⠀⠀⠀", row=1, style=ButtonStyle.success)
    async def create_room(self, interaction, button):
        bucket = self.cooldown.get_bucket(interaction.message)
        retry = bucket.update_rate_limit()
        if retry:
            return await interaction.response.send_message(
                embed=get_slow_down_embed(self.bot, round(retry, 1)), ephemeral=True
            )
        user_id = interaction.user.id
        has_room = await self.bot.database.is_owner(user_id)
        if has_room:
            await interaction.response.send_message(
                embed=get_you_already_has_room_embed(self.bot), ephemeral=True
            )
        else:
            await interaction.response.send_modal(CreateRoomModal(self.bot, interaction.user.name))

    @ui.button(label="DELETE", row=1, style=ButtonStyle.red)
    async def delete(self, interaction, button):
        has_room = await self.bot.database.is_owner(interaction.user.id)
        if has_room:
            user_room_id = await self.bot.database.get_user_room_id(interaction.user.id)
            guild = self.bot.get_guild(self.bot.config["GUILD_ID"])
            user_room = get(guild.voice_channels, id=user_room_id)
            await self.bot.database.delete_user_room(user_id=interaction.user.id)
            await user_room.delete()
            await interaction.response.send_message(
                embed=get_deleted_embed(self.bot), ephemeral=True
            )
        else:
            await interaction.response.send_message(
                embed=get_havent_room_embed(self.bot), ephemeral=True
            )


# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot) -> None:
    await bot.add_cog(SelfRooms(bot))
