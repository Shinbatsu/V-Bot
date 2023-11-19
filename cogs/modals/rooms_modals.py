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
        self.guild = self.bot.get_guild(self.bot.config["GUILD_ID"])

    async def on_submit(self, interaction) -> None:
        await interaction.response.defer() 
        try:
            person_id = int(self.person_id.value)
            guild = self.bot.get_guild(self.bot.config["GUILD_ID"])
            member = guild.get_member(person_id)
            if not member.voice:
                await interaction.followup.send(
                    embed=get_unknown_member_embed(self.bot, member.name), ephemeral=True
                )
                return
            member_channel_id = member.voice.channel.id or None
            room_who_wanna_kick = await self.bot.database.get_user_room_id(interaction.user.id)
            if person_id == interaction.user.id:
                await interaction.followup.send(
                    embed=get_kick_self_embed(self.bot), ephemeral=True
                )
            if room_who_wanna_kick == member_channel_id:
                await member.edit(voice_channel=None)
                await interaction.followup.send(
                    embed=get_kick_embed(self.bot, member.name), ephemeral=True
                )
            else:
                await interaction.followup.send(
                    embed=get_havent_rights_embed(self.bot, member.name), ephemeral=True
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

    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.guild = self.bot.get_guild(self.bot.config["GUILD_ID"])

    async def on_submit(self, interaction) -> None:
        await interaction.response.defer()  
        try:
            new_owner_id = int(self.new_owner_id.value)
            guild = self.bot.get_guild(self.bot.config["GUILD_ID"])
            member = guild.get_member(new_owner_id)
        except ValueError:
            await interaction.followup.send(
                embed=get_unknown_member_embed(self.bot, new_owner_id), ephemeral=True
            )
        is_already_owner = await self.bot.database.is_owner(member.id)
        if is_already_owner:
            await interaction.followup.send(
                embed=get_another_user_already_has_room_embed(self.bot, member.name), ephemeral=True
            )
        else:
            user_room_id = await self.bot.database.get_user_room_id(interaction.user.id)
            user_room = self.bot.get_channel(user_room_id)
            invite_link = await user_room.create_invite(unique=True)
            await self.bot.database.change_room_owner(room_id=user_room_id, user_id=member.id)
            await member.send(embed=get_room_link_embed(self.bot, invite_link.url))
            await interaction.followup.send(
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

    def __init__(self, bot, username):
        super().__init__()
        self.bot = bot
        self.guild = self.bot.get_guild(self.bot.config["GUILD_ID"])
        self.username = username
        self.room_name.default = f"{username}'s room"

    async def on_submit(self, interaction) -> None:
        await interaction.response.defer()
        mute_role =[*filter(lambda role: role.name == "M", self.guild.roles)][0]
        untype_role = [*filter(lambda role: role.name == "T", self.guild.roles)][0]
        ban_role = [*filter(lambda role: role.name == "B", self.guild.roles)][0]
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
        category = [*filter(lambda category: category.id == self.bot.config["ACTIVE_NOW_CATEGORY_ID"], self.guild.categories)][0]
        user_room = await interaction.guild.create_voice_channel(
            room_name,
            category=category,
            user_limit=room_slots,
        )
        await user_room.edit(overwrites=overwrites)
        await self.bot.database.add_user_room(interaction.user.id, user_room.id, room_name)
        invite_link = await user_room.create_invite(unique=True)
        await interaction.user.send(embed=get_room_link_embed(self.bot, invite_link.url))
        await interaction.followup.send(
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
        await interaction.response.defer()
        new_name = self.new_name.value
        user_room_id = await self.bot.database.get_user_room_id(user_id=interaction.user.id)
        user_room = self.bot.get_channel(user_room_id)
        await user_room.edit(name=new_name)
        await self.bot.database.rename_user_room(room_id=user_room_id, new_room_name=new_name)
        await interaction.followup.send(
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
        self.guild = self.bot.get_guild(self.bot.config["GUILD_ID"])

    async def on_submit(self, interaction) -> None:
        await interaction.response.defer()
        try:
            t = int(self.new_user_limit.value)
            new_user_limit = [[t, 1], [20, t]][t > 20][t < 1]
        except ValueError:
            await interaction.followup.send(
                embed=get_unknown_value_embed(self.bot, new_user_limit.value), ephemeral=True
            )

        user_room_id = await self.bot.database.get_user_room_id(user_id=interaction.user.id)
        user_room = self.bot.get_channel(user_room_id)
        await user_room.edit(user_limit=new_user_limit)
        await interaction.followup.send(
            embed=get_change_user_limit_room_embed(self.bot, new_user_limit), ephemeral=True
        )
def get_pick_rank_embed(bot: Client) -> Embed:
    embed = Embed(
        title="Получить ваш Valorant ранг",
        color=Colour.from_str(bot.config["INFO_COLOR"]),
    )
    embed.add_field(
        name="""<:minidot:1174667819917520966> Укажите ваше название профиля: ```NAME#0000```. """,
        value="",
        inline=False,
    )
    embed.add_field(
        name="",
        value="""```В случае если указанный вами ник кем-то занят, обратитесь в модерацию.Виновник понесет несовместимое с присутсвием на сервере наказание!```""",
        inline=False,
    )
    embed.add_field(
        name="",
        value="""```В случае если вы решили сменить ваш RIOT аккаунт и хотите обновить ник обратитесь в модерацию.```""",
        inline=False,
    )
    embed.add_field(
        name="",
        value="""```В случае если вы решили сменить ваш RIOT аккаунт и хотите обновить ник обратитесь в модерацию.```""",
        inline=False,
    )

    embed.add_field(
        name="",
        value="ПРИМЕЧАНИЕ: В целях дополнительной верификации ник можно указать только 1 раз для 1-го аккаунта!",
    )
    return embed


def get_different_nicknames_embed(bot: Client, nick: str, repeat_nick: str) -> Embed:
    embed = Embed(
        title="Введенные формы не совпадают!",
        color=Colour.from_str(bot.config["ERROR_COLOR"]),
    )
    embed.add_field(
        name="```Name:```",
        value=f"""```{nick}```""",
    )
    embed.add_field(
        name="Name repeat:",
        value=f"""```{repeat_nick}```""",
    )
    return embed


def get_already_has_nickname_embed(bot: Client, nick: str) -> Embed:
    embed = Embed(
        title="Ник уже занят!",
        color=Colour.from_str(bot.config["ERROR_COLOR"]),
    )
    embed.add_field(
        name="",
        value=f"Пользователь {nick} уже использует это имя!",
    )
    return embed


def get_you_got_rank_embed(bot: Client, username: str, rank: str) -> Embed:
    embed = Embed(
        title="Ваш ранг успешно добавлен!",
        color=Colour.from_str(bot.config["SUCCESS_COLOR"]),
    )
    embed.add_field(
        name=f"Поздравляем! {username.capitalize()}! Теперь у вас есть Valorant ранг:",
        value=f"{rank}",
    )
    return embed


def get_you_update_rank_embed(bot: Client, username: str, rank: str) -> Embed:
    embed = Embed(
        title="Ваш ранг успешно обновлен!",
        color=Colour.from_str(bot.config["SUCCESS_COLOR"]),
    )
    embed.add_field(name=f"{username.capitalize()}, Теперь ваш Valorant ранг:", value=f"{rank}")
    return embed


def get_cant_get_rank_embed(bot: Client) -> Embed:
    embed = Embed(
        title="Не удалось получить ранг!",
        color=Colour.from_str(bot.config["ERROR_COLOR"]),
    )
    embed.add_field(name="Произошла ошибка присвоения ранга, попробуйте позже!", value="")
    return embed


def get_cant_update_rank_embed(bot: Client) -> Embed:
    embed = Embed(
        title="Не удалось обновить ранг!",
        color=Colour.from_str(bot.config["ERROR_COLOR"]),
    )
    embed.add_field(name="Произошла ошибка обновления ранга, попробуйте позже!", value="")
    return embed


def get_cant_update_rank_embed(bot: Client) -> Embed:
    embed = Embed(
        title="Не удалось обновить ранг!",
        color=Colour.from_str(bot.config["ERROR_COLOR"]),
    )
    embed.add_field(name="У вас пока что нет ранга!", value="")
    return embed
