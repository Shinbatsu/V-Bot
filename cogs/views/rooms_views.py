from discord import ButtonStyle
from discord.ui import View, button
from discord.ext import commands
from discord import PartialEmoji, ButtonStyle, PermissionOverwrite

from ..embeds.rooms_embed import *
from ..modals.rooms_modals import *


class RoomSettingsView(
    View,
):
    def __init__(self, database):
        super().__init__(timeout=None)
        self.database = database
        self.cooldown = commands.CooldownMapping.from_cooldown(1, 15, commands.BucketType.member)
        self.cooldown_mini = commands.CooldownMapping.from_cooldown(
            1, 5, commands.BucketType.member
        )

    @button(
        label="",
        emoji=PartialEmoji.from_str("<:custom_lock:1173271460970758204>"),
        row=0,
        style=ButtonStyle.secondary,
        custom_id="RoomSettingsView:lock",
    )
    async def lock(self, interaction, button):
        await interaction.response.defer(ephemeral=True)
        bucket = self.cooldown_mini.get_bucket(interaction.message)
        retry = bucket.update_rate_limit()
        if retry:
            return await interaction.followup.send(
                embed=get_slow_down_embed(round(retry, 1)), ephemeral=True
            )
        member = interaction.user
        is_owner = await self.database.is_owner(interaction.user.id)
        if is_owner:
            is_closed = await self.database.get_is_closed_room(user_id=interaction.user.id)
            user_room_id = await self.database.get_user_room_id(interaction.user.id)
            guild = interaction.guild.id
            user_room = interaction.guild.get_channel(user_room_id)
            if not is_closed:
                await user_room.edit(
                    overwrites={
                        member: PermissionOverwrite(connect=False),
                        guild.default_role: PermissionOverwrite(connect=False),
                    }
                )
                await interaction.followup.send(embed=get_room_closed_embed(), ephemeral=True)
                await self.database.update_is_close_user_room(room_id=user_room_id, is_close=True)
            else:
                await user_room.edit(
                    overwrites={
                        member: PermissionOverwrite(connect=True),
                        guild.default_role: PermissionOverwrite(connect=True),
                    }
                )
                await interaction.followup.send(embed=get_room_opened_embed(), ephemeral=True)
                await self.database.update_is_close_user_room(room_id=user_room_id, is_close=False)
        else:
            await interaction.response.send_message(embed=get_havent_room_embed(), ephemeral=True)

    @button(
        label="",
        emoji=PartialEmoji.from_str("<:kick:1173271463244087336>"),
        row=0,
        style=ButtonStyle.secondary,
        custom_id="RoomSettingsView:kick",
    )
    async def kick(self, interaction, button):
        has_room = await self.database.is_owner(interaction.user.id)
        if has_room:
            await interaction.response.send_modal(KickModal(self.database))
            return
        else:
            await interaction.response.defer(ephemeral=True)
            await interaction.response.send_message(embed=get_havent_room_embed(), ephemeral=True)

    @button(
        label="",
        emoji=PartialEmoji.from_str("<:slots:1173271467060904050>"),
        row=0,
        style=ButtonStyle.secondary,
        custom_id="RoomSettingsView:slots",
    )
    async def slots(self, interaction, button):
        has_room = await self.database.is_owner(interaction.user.id)
        if has_room:
            await interaction.response.send_modal(ChangeSlotsModal(self.database))
        else:
            await interaction.response.defer(ephemeral=True)
            await interaction.followup.send(embed=get_havent_room_embed(), ephemeral=True)

    @button(
        label="",
        row=0,
        emoji=PartialEmoji.from_str("<:change_owner:1173271455786602526>"),
        style=ButtonStyle.secondary,
        custom_id="RoomSettingsView:change_owner",
    )
    async def change_owner(self, interaction, button):
        has_room = await self.database.is_owner(interaction.user.id)
        if has_room:
            await interaction.response.send_modal(ChangeOwnerModal(self.database))
        else:
            await interaction.response.defer(ephemeral=True)
            await interaction.followup.send(embed=get_havent_room_embed(), ephemeral=True)

    @button(
        label="",
        row=0,
        emoji=PartialEmoji.from_str("<:rename:1173271464699498677>"),
        style=ButtonStyle.secondary,
        custom_id="RoomSettingsView:rename",
    )
    async def rename(self, interaction, button):
        has_room = await self.database.is_owner(interaction.user.id)
        if has_room:
            return await interaction.response.send_modal(RenameRoomModal(self.database))
        else:
            await interaction.response.defer(ephemeral=True)
            await interaction.followup.send(embed=get_havent_room_embed(), ephemeral=True)

    @button(
        label="⠀⠀CREATE ROOM⠀⠀",
        row=1,
        style=ButtonStyle.success,
        custom_id="RoomSettingsView:create_room",
    )
    async def create_room(self, interaction, button):
        bucket = self.cooldown.get_bucket(interaction.message)
        retry = bucket.update_rate_limit()
        if retry:
            return await interaction.followup.send(
                embed=get_slow_down_embed(round(retry, 1)), ephemeral=True
            )
        user_id = interaction.user.id
        has_room = await self.database.is_owner(user_id)
        if has_room:
            await interaction.response.defer(ephemeral=True)
            return await interaction.followup.send(
                embed=get_you_already_has_room_embed(), ephemeral=True
            )
        else:
            await interaction.response.send_modal(CreateRoomModal(self.database, interaction.user.name))

    @button(
        label="⠀DELETE⠀⠀",
        row=1,
        style=ButtonStyle.red,
        custom_id="RoomSettingsView:delete",
    )
    async def delete(self, interaction, button):
        await interaction.response.defer(ephemeral=True)
        has_room = await self.database.is_owner(interaction.user.id)
        if has_room:
            user_room_id = await self.database.get_user_room_id(interaction.user.id)
            user_room = interaction.guild.get_channel(user_room_id)
            await self.database.delete_user_room(user_id=interaction.user.id)
            if user_room:
                await user_room.delete()
                await interaction.followup.send(embed=get_room_deleted_embed(), ephemeral=True)
        else:
            await interaction.followup.send(embed=get_havent_room_embed(), ephemeral=True)

    @button(
        label="UP",
        row=1,
        style=ButtonStyle.grey,
        custom_id="RoomSettingsView:up",
    )
    async def up(self, interaction, button):
        await interaction.response.defer(ephemeral=True)
        bucket = self.cooldown.get_bucket(interaction.message)
        retry = bucket.update_rate_limit()
        if retry:
            return await interaction.followup.send(
                embed=get_slow_down_embed(round(retry, 1)), ephemeral=True
            )
        has_room = await self.database.is_owner(interaction.user.id)
        if has_room:
            user_room_id = await self.database.get_user_room_id(interaction.user.id)
            user_room = interaction.guild.get_channel(user_room_id)
            await user_room.edit(position=0)
            await interaction.followup.send(embed=get_room_upped_embed(), ephemeral=True)
        else:
            await interaction.followup.send(embed=get_havent_room_embed(), ephemeral=True)
