from discord import ButtonStyle
from discord.ui import View, button
from discord.ext import commands
from discord import ui, PartialEmoji, ButtonStyle, PermissionOverwrite
from discord.ui import View, button

from ..embeds.rooms_embed import *
from ..modals.rooms_modals import *


class RoomSettingsView(
    View,
):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.cooldown = commands.CooldownMapping.from_cooldown(1, 60, commands.BucketType.member)
        self.guild = self.bot.get_guild(self.bot.config["GUILD_ID"])

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
            user_room = self.bot.get_channel(user_room_id)
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

    @button(label="⠀⠀CREATE ROOM⠀⠀", row=1, style=ButtonStyle.success)
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

    @ui.button(label="⠀DELETE⠀⠀", row=1, style=ButtonStyle.red)
    async def delete(self, interaction, button):
        has_room = await self.bot.database.is_owner(interaction.user.id)
        if has_room:
            user_room_id = await self.bot.database.get_user_room_id(interaction.user.id)
            guild = self.bot.get_guild(self.bot.config["GUILD_ID"])
            user_room = self.bot.get_channel(user_room_id)
            await self.bot.database.delete_user_room(user_id=interaction.user.id)
            await user_room.delete()
            await interaction.response.send_message(
                embed=get_room_deleted_embed(self.bot), ephemeral=True
            )
        else:
            await interaction.response.send_message(
                embed=get_havent_room_embed(self.bot), ephemeral=True
            )

    @ui.button(label="UP", row=1, style=ButtonStyle.grey)
    async def up(self, interaction, button):
        has_room = await self.bot.database.is_owner(interaction.user.id)
        if has_room:
            user_room_id = await self.bot.database.get_user_room_id(interaction.user.id)
            guild = self.bot.get_guild(self.bot.config["GUILD_ID"])
            user_room = self.bot.get_channel(user_room_id)
            await user_room.edit(position=0)
            await interaction.response.send_message(
                embed=get_room_upped_embed(self.bot), ephemeral=True
            )
        else:
            await interaction.response.send_message(
                embed=get_havent_room_embed(self.bot), ephemeral=True
            )