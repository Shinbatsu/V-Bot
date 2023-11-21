from discord import TextStyle, PermissionOverwrite
from discord.ui import TextInput, Modal, button
from ..embeds.rooms_embed import *


class KickModal(Modal, title="Изгнать пользователя"):
    person_id = TextInput(
        label="Введите ID пользователя или уникальное имя:",
        placeholder="",
        default="",
        style=TextStyle.short,
        required=False,
        max_length=20,
    )

    def __init__(self, database):
        super().__init__(timeout=None)
        self.database = database

    def get_member_by_name(self, guild, username):
        for member in guild.members:
            if member.name == username:
                return member

    async def on_submit(self, interaction) -> None:
        await interaction.response.defer(ephemeral=True)
        try:
            if self.person_id.value.isdigit():
                person_id = interaction.guild.get_member(int(self.reported_user.value)).id
            else:
                person_id = self.get_member_by_name(interaction.guild, self.reported_user.value).id
            member = interaction.guild.get_member(person_id)
            if not member.voice:
                await interaction.followup.send(
                    embed=get_unknown_member_embed(member.name), ephemeral=True
                )
                return
            member_channel_id = member.voice.channel.id or None
            room_who_wanna_kick = await self.database.get_user_room_id(interaction.user.id)
            if person_id == interaction.user.id:
                await interaction.followup.send(embed=get_kick_self_embed(), ephemeral=True)
            if room_who_wanna_kick == member_channel_id:
                await member.edit(voice_channel=None)
                await interaction.followup.send(embed=get_kick_embed(member.name), ephemeral=True)
            else:
                await interaction.followup.send(
                    embed=get_havent_rights_embed(member.name), ephemeral=True
                )
        except ValueError:
            await interaction.followup.send("Пользователь не найден!", ephemeral=True)
            return


class ChangeOwnerModal(Modal, title="Изменение владельца"):
    new_owner_id = TextInput(
        label="Введите ID нового владельца:",
        placeholder="",
        default="",
        style=TextStyle.short,
        required=True,
        max_length=20,
    )

    def __init__(self, database):
        super().__init__()
        self.database = database

    async def on_submit(self, interaction) -> None:
        await interaction.response.defer(ephemeral=True)
        try:
            new_owner_id = int(self.new_owner_id.value)
            guild = interaction.guild
            member = guild.get_member(new_owner_id)
        except ValueError:
            await interaction.followup.send(
                embed=get_unknown_member_embed(new_owner_id), ephemeral=True
            )
        is_already_owner = await self.database.is_owner(member.id)
        if is_already_owner:
            await interaction.followup.send(
                embed=get_another_user_already_has_room_embed(member.name), ephemeral=True
            )
        else:
            user_room_id = await self.database.get_user_room_id(interaction.user.id)
            user_room = interaction.guild.get_channel(user_room_id)
            invite_link = await user_room.create_invite(unique=True)
            await self.database.change_room_owner(room_id=user_room_id, user_id=member.id)
            await member.send(embed=get_room_link_embed(invite_link.url))
            await interaction.followup.send(embed=get_new_owner_embed(member.name), ephemeral=True)


class CreateRoomModal(Modal, title="Название комнаты"):
    room_name = TextInput(
        label="Введите название комнаты:",
        placeholder="Your room",
        default="",
        style=TextStyle.short,
        required=False,
        max_length=30,
    )
    slots = TextInput(
        label="Введите размер комнаты:",
        placeholder="1-20",
        default=5,
        style=TextStyle.short,
        required=False,
        max_length=2,
    )

    def __init__(self, database, username):
        super().__init__()
        self.database = database
        self.username = username
        self.room_name.default = f"{username}'s room"

    async def on_submit(self, interaction) -> None:
        await interaction.response.defer(ephemeral=True)
        mute_role = [*filter(lambda role: role.name == "M", interaction.guild.roles)][0]
        untype_role = [*filter(lambda role: role.name == "T", interaction.guild.roles)][0]
        ban_role = [*filter(lambda role: role.name == "B", interaction.guild.roles)][0]
        overwrites = {
            mute_role: PermissionOverwrite(speak=False),
            untype_role: PermissionOverwrite(send_messages=False),
            ban_role: PermissionOverwrite(
                create_instant_invite=False,
                kick_members=False,
                ban_members=False,
                administrator=False,
                manage_channels=False,
                manage_guild=False,
                add_reactions=False,
                view_audit_log=False,
                priority_speaker=False,
                stream=False,
                read_messages=False,
                view_channel=False,
                send_messages=False,
                send_tts_messages=False,
                manage_messages=False,
                embed_links=False,
                attach_files=False,
                read_message_history=False,
                mention_everyone=False,
                external_emojis=False,
                use_external_emojis=False,
                view_guild_insights=False,
                connect=False,
                speak=False,
                mute_members=False,
                deafen_members=False,
                move_members=False,
                use_voice_activation=False,
                change_nickname=False,
                manage_nicknames=False,
                manage_roles=False,
                manage_permissions=False,
                manage_webhooks=False,
                manage_emojis=False,
                manage_emojis_and_stickers=False,
                use_application_commands=False,
                request_to_speak=False,
                manage_events=False,
                manage_threads=False,
                create_public_threads=False,
                create_private_threads=False,
                send_messages_in_threads=False,
                external_stickers=False,
                use_external_stickers=False,
                use_embedded_activities=False,
                moderate_members=False,
            ),
        }

        try:
            room_slots = int(self.slots.value) if self.slots.value else 5
        except ValueError:
            room_slots = 5
        try:
            room_name = str(self.room_name.value) or f"{self.username}'s room"
        except room_slots:
            room_name = f"{self.username}'s room"
        category = [
            *filter(
                lambda category: category.id == 1174053375948640437,
                interaction.guild.categories,
            )
        ][0]
        user_room = await interaction.guild.create_voice_channel(
            room_name,
            category=category,
            user_limit=room_slots,
        )
        await user_room.edit(overwrites=overwrites)
        await self.database.add_user_room(interaction.user.id, user_room.id, room_name)
        invite_link = await user_room.create_invite(unique=True)
        await interaction.user.send(embed=get_room_link_embed(invite_link.url))
        await interaction.followup.send(embed=get_created_room_embed(), ephemeral=True)


class RenameRoomModal(Modal, title="Переименование канала"):
    new_name = TextInput(
        label="Введите новое название комнаты:",
        placeholder="Новое название",
        default="",
        style=TextStyle.short,
        required=True,
        max_length=30,
    )

    def __init__(self, database):
        super().__init__()
        self.database = database

    async def on_submit(self, interaction) -> None:
        await interaction.response.defer(ephemeral=True)
        new_name = self.new_name.value
        user_room_id = await self.database.get_user_room_id(user_id=interaction.user.id)
        user_room = interaction.guild.get_channel(user_room_id)
        await user_room.edit(name=new_name)
        await self.database.rename_user_room(room_id=user_room_id, new_room_name=new_name)
        await interaction.followup.send(
            embed=get_rename_room_embed(new_name), ephemeral=True
        )


class ChangeSlotsModal(Modal, title="Изменение количества участников"):
    new_user_limit = TextInput(
        label="Введите новое количество участников:",
        placeholder="1-20",
        default="",
        style=TextStyle.short,
        required=True,
        max_length=2,
    )

    def __init__(self, database):
        super().__init__()
        self.database = database

    async def on_submit(self, interaction) -> None:
        await interaction.response.defer(ephemeral=True)
        try:
            t = int(self.new_user_limit.value)
            new_user_limit = [[t, 1], [20, t]][t > 20][t < 1]
        except ValueError:
            await interaction.followup.send(
                embed=get_unknown_value_embed(new_user_limit.value), ephemeral=True
            )

        user_room_id = await self.database.get_user_room_id(user_id=interaction.user.id)
        user_room = self.get_channel(user_room_id)
        await user_room.edit(user_limit=new_user_limit)
        await interaction.followup.send(
            embed=get_change_user_limit_room_embed(new_user_limit), ephemeral=True
        )