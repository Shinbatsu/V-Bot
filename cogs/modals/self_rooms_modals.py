from discord import TextStyle
from discord.ui import TextInput, Modal, button
from discord.utils import get
from ..embeds.self_rooms_embed import *


class KickModal(Modal, title="Изгнать пользователя"):
    person_id = TextInput(
        label="Введите ID пользователя:",
        placeholder="",
        default="",
        style=TextStyle.short,
        required=False,
        max_length=20,
    )
    persons_ids = TextInput(
        label="Участники Комнаты",
        placeholder="",
        default="",
        style=TextStyle.paragraph,
        required=False,
        max_length=4000,
    )

    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    async def on_submit(self, interaction) -> None:
        try:
            person_id = int(self.person_id.value)
            guild = self.bot.get_guild(self.bot.config["GUILD_ID"])
            member = guild.get_member(person_id)
            if not member.voice:
                await interaction.response.send_message(
                    embed=get_unknown_member_embed(self.bot, member.name), ephemeral=True
                )
                return
            member_channel_id = member.voice.channel.id or None
            room_who_wanna_kick = await self.bot.database.get_user_room_id(interaction.user.id)
            if person_id == interaction.user.id:
                await interaction.response.send_message(
                    embed=get_kick_self_embed(self.bot), ephemeral=True
                )
            if room_who_wanna_kick == member_channel_id:
                await member.edit(voice_channel=None)
                await interaction.response.send_message(
                    embed=get_kick_embed(self.bot, member.name), ephemeral=True
                )
            else:
                await interaction.response.send_message(
                    embed=get_havent_rights_embed(self.bot, member.name), ephemeral=True
                )
        except ValueError:
            await interaction.response.send_message("Пользователь не найден!", ephemeral=True)
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

    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    async def on_submit(self, interaction) -> None:
        try:
            new_owner_id = int(self.new_owner_id.value)
            guild = self.bot.get_guild(self.bot.config["GUILD_ID"])
            member = guild.get_member(new_owner_id)
        except ValueError:
            await interaction.response.send_message(
                embed=get_unknown_member_embed(self.bot, new_owner_id), ephemeral=True
            )
        is_already_owner = await self.bot.database.is_owner(member.id)
        if is_already_owner:
            await interaction.response.send_message(
                embed=get_another_user_already_has_room_embed(self.bot, member.name), ephemeral=True
            )
        else:
            user_room_id = await self.bot.database.get_user_room_id(interaction.user.id)
            user_room = get(guild.voice_channels, id=user_room_id)
            invite_link = await user_room.create_invite(unique=True)
            await self.bot.database.change_room_owner(room_id=user_room_id, user_id=member.id)
            await member.send(embed=get_room_link_embed(self.bot, invite_link.url))
            await interaction.response.send_message(
                embed=get_new_owner_embed(self.bot, member.name), ephemeral=True
            )


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

    def __init__(self, bot, user_name):
        super().__init__()
        self.bot = bot
        self.user_name = user_name
        self.room_name.default = f"{user_name}'s room"

    async def on_submit(self, interaction) -> None:
        try:
            room_slots = int(self.slots.value) if self.slots.value else 5
        except ValueError:
            room_slots = 5
        try:
            room_name = str(self.room_name.value) or f"{self.user_name}'s room"
        except room_slots:
            room_name = f"{self.user_name}'s room"
        category = get(interaction.guild.categories, id=self.bot.config["ACTIVE_NOW_CATEGORY_ID"])
        user_room = await interaction.guild.create_voice_channel(
            room_name,
            category=category,
            user_limit=room_slots,
        )
        await self.bot.database.add_user_room(interaction.user.id, user_room.id, room_name)
        invite_link = await user_room.create_invite(unique=True)
        await interaction.user.send(embed=get_room_link_embed(self.bot, invite_link.url))
        await interaction.response.send_message(
            embed=get_created_room_embed(self.bot), ephemeral=True
        )


class RenameRoomModal(Modal, title="Переименование канала"):
    new_name = TextInput(
        label="Введите новое название комнаты:",
        placeholder="Новое название",
        default="",
        style=TextStyle.short,
        required=True,
        max_length=30,
    )

    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    async def on_submit(self, interaction) -> None:
        new_name = self.new_name.value

        guild = self.bot.get_guild(self.bot.config["GUILD_ID"])
        user_room_id = await self.bot.database.get_user_room_id(user_id=interaction.user.id)
        user_room = get(guild.voice_channels, id=user_room_id)
        await user_room.edit(name=new_name)
        await self.bot.database.rename_user_room(room_id=user_room_id, new_room_name=new_name)
        await interaction.response.send_message(
            embed=get_rename_room_embed(self.bot, new_name), ephemeral=True
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

    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    async def on_submit(self, interaction) -> None:
        try:
            t = int(self.new_user_limit.value)
            new_user_limit = [[t, 1], [20, t]][t > 20][t < 1]
        except ValueError:
            await interaction.response.send_message(
                embed=get_unknown_value_embed(self.bot, new_user_limit.value), ephemeral=True
            )

        guild = self.bot.get_guild(self.bot.config["GUILD_ID"])
        user_room_id = await self.bot.database.get_user_room_id(user_id=interaction.user.id)
        user_room = get(guild.voice_channels, id=user_room_id)
        await user_room.edit(user_limit=new_user_limit)
        await interaction.response.send_message(
            embed=get_change_user_limit_room_embed(self.bot, new_user_limit), ephemeral=True
        )
