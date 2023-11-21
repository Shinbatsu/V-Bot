from discord.ui import View, select, Modal, TextInput
from ..embeds.ticket_embed import *
from discord import TextStyle, SelectOption
from discord.ext import commands
import asyncio


class CreateReportModal(Modal, title="Создание жалобы"):
    reported_user = TextInput(
        label="Введите ID пользователя или уникальное имя",
        placeholder="Пример: 383943093310980096",
        default="",
        style=TextStyle.short,
        required=True,
        max_length=50,
    )
    description = TextInput(
        label="Причина",
        placeholder="Подробно опишите причину...",
        default="",
        style=TextStyle.paragraph,
        required=True,
        max_length=512,
    )

    def __init__(self, database):
        super().__init__()
        self.database = database

    def get_member_by_name(self, guild, username):
        for member in guild.members:
            if member.name == username:
                return member

    async def on_submit(self, interaction) -> None:
        if self.reported_user.value.isdigit():
            self.reported_user = interaction.guild.get_member(int(self.reported_user.value))
        else:
            self.reported_user = self.get_member_by_name(
                interaction.guild, self.reported_user.value
            )
        if self.reported_user.id == interaction.user.id:
            await interaction.response.defer()
            await interaction.followup.send(embed=get_report_sent_embed(), ephemeral=True)
        report_channel = interaction.guild.get_channel(1171364238330179635)
        description = self.description.value
        message = await report_channel.send(".")
        message_url = message.jump_url
        await message.edit(
            embed=get_report_info_embed(
                interaction.user.name, self.reported_user.name, description
            ),
            view=ModeratorActionView(self.reported_user, message_url),
        )
        await interaction.response.defer()
        await interaction.followup.send(embed=get_report_sent_embed(), ephemeral=True)


class ModeratorActionView(View):
    def __init__(self, database, user_to_action, message_url):
        super().__init__()
        self.database = database
        self.user_to_action = user_to_action
        self.message_url = message_url

    @select(
        placeholder="Выбери действие",
        min_values=1,
        max_values=1,
        options=[
            SelectOption(label="Закрыть жалобу"),
            SelectOption(label="Отправить предупреждение"),
            SelectOption(label="Кик"),
            SelectOption(label="Временный мут"),
            SelectOption(label="Временный запрет печати"),
            SelectOption(label="Временный бан"),
            SelectOption(label="Вечный Бан-хаммер"),
        ],
    )
    async def action(self, interaction, select):
        user_pick = select.values[0]
        if user_pick == "Закрыть жалобу":
            self.action.disabled = True
            await interaction.response.defer()
            await interaction.followup.send(
                embed=get_report_was_resolved_embed(
                    self.message_url, interaction.user.name
                )
            )
        elif user_pick == "Отправить предупреждение":
            await interaction.response.send_modal(UserWarnModal(self.database, self.user_to_action))
        elif user_pick == "Кик":
            await interaction.response.send_modal(UserKickModal(self.database, self.user_to_action))
        elif user_pick == "Временный мут":
            await interaction.response.send_modal(TempMuteModal(self.database, self.user_to_action))
        elif user_pick == "Временный запрет печати":
            await interaction.response.send_modal(TempStopTypingModal(self.database, self.user_to_action)
            )
        elif user_pick == "Временный бан":
            await interaction.response.send_modal(TempBanModal(self.database, self.user_to_action))
        elif user_pick == "Бан-хаммер":
            await interaction.response.send_modal(
                BanForeverModal(self.database, self.user_to_action)
            )


class UserWarnModal(Modal, title="Замечание"):
    description = TextInput(
        label="Причина",
        placeholder="Аргументация",
        default="Вам выдано замечание в связи с жалобами!",
        style=TextStyle.paragraph,
        required=True,
        max_length=512,
    )

    def __init__(self, database, user_to_warn):
        super().__init__()
        self.database = database
        self.user_to_warn = user_to_warn

    async def on_submit(self, interaction) -> None:
        description = self.description.value
        await interaction.response.defer()
        await self.user_to_warn.send(embed=get_user_warn_embed(description))
        await interaction.followup.send(embed=get_user_warn_sent_embed(), ephemeral=True)


class UserKickModal(Modal, title="Кик"):
    description = TextInput(
        label="Причина",
        placeholder="Аргументация",
        default="Вас кикнули с сервера в связи с жалобами!",
        style=TextStyle.paragraph,
        required=True,
        max_length=512,
    )

    def __init__(self, database, user_to_kick):
        super().__init__()
        self.database = database
        self.user_to_kick = user_to_kick

    async def on_submit(self, interaction) -> None:
        await interaction.response.defer()
        description = self.description.value
        await self.user_to_kick.send(embed=get_user_kick_embed(description))
        await interaction.followup.send(embed=get_user_kick_sent_embed(), ephemeral=True)


class TempMuteModal(Modal, title="Временный мут"):
    seconds = TextInput(
        label="Количество секунд",
        placeholder="Время",
        default="3600",
        style=TextStyle.short,
        required=True,
        max_length=10,
    )
    description = TextInput(
        label="Причина",
        placeholder="Аргументация",
        default="Вам выдан временный мут в связи с жалобами!",
        style=TextStyle.paragraph,
        required=True,
        max_length=512,
    )

    def __init__(self, database, user_to_mute):
        super().__init__()
        self.database = database
        self.user_to_mute = user_to_mute

    async def on_submit(self, interaction) -> None:
        await interaction.response.defer()
        description = self.description.value
        mute_role = [*filter(lambda role: role.name == "M", interaction.guild.roles)][0]
        await self.user_to_mute.add_roles(mute_role)
        time = int(self.seconds.value)
        await self.user_to_mute.send(embed=get_user_temp_mute_embed(description, time))
        await interaction.followup.send(embed=get_user_temp_mute_sent_embed(), ephemeral=True)
        await asyncio.sleep(time)
        await self.user_to_mute.remove_roles(mute_role)
        await self.user_to_mute.send(embed=get_user_unmute_embed())


class TempStopTypingModal(Modal, title="Временный запрет печати"):
    seconds = TextInput(
        label="Количество секунд",
        placeholder="Время",
        default="3600",
        style=TextStyle.short,
        required=True,
        max_length=10,
    )
    description = TextInput(
        label="Причина",
        placeholder="Аргументация",
        default="Вам выдан запрет печати в связи с жалобами!",
        style=TextStyle.paragraph,
        required=True,
        max_length=512,
    )

    def __init__(self, database, user_to_stop_typing):
        super().__init__()
        self.database = database
        self.user_to_stop_typing = user_to_stop_typing

    async def on_submit(self, interaction) -> None:
        await interaction.response.defer()
        description = self.description.value
        stop_typing_role = [*filter(lambda role: role.name == "T", interaction.guild.roles)][0]
        await self.user_to_stop_typing.add_roles(stop_typing_role)
        time = int(self.seconds.value)
        await self.user_to_stop_typing.send(
            embed=get_user_temp_stop_typing_embed(description, time)
        )
        await interaction.followup.send(
            embed=get_user_temp_stop_typing_sent_embed(), ephemeral=True
        )
        await asyncio.sleep(time)
        await self.user_to_stop_typing.remove_roles(stop_typing_role)
        await self.user_to_stop_typing.send(embed=get_user_temp_unstop_typing_embed())


class TempBanModal(Modal, title="Временный бан"):
    seconds = TextInput(
        label="Количество секунд",
        placeholder="Время",
        default="3600",
        style=TextStyle.short,
        required=True,
        max_length=10,
    )
    description = TextInput(
        label="Причина",
        placeholder="Аргументация",
        default="Вам выдана временная блокировка в связи с жалобами!",
        style=TextStyle.paragraph,
        required=True,
        max_length=512,
    )

    def __init__(self, database, user_to_ban):
        super().__init__()
        self.database = database
        self.user_to_ban = user_to_ban

    async def on_submit(self, interaction) -> None:
        await interaction.response.defer()
        description = self.description.value
        temp_ban_role = [*filter(lambda role: role.name == "B", interaction.guild.roles)][0]
        await self.user_to_ban.add_roles(temp_ban_role)
        time = int(self.seconds.value)
        await self.user_to_ban.send(embed=get_user_temp_stop_typing_embed(description, time))
        lp_room = interaction.guild.get_channel(1175538192582193222)
        await self.user_to_ban.edit(voice_channel=lp_room)
        await interaction.followup.send(embed=get_user_temp_ban_sent_embed(), ephemeral=True)
        await asyncio.sleep(time)
        await self.user_to_ban.remove_roles(temp_ban_role)
        await self.user_to_ban.send(embed=get_user_unban_embed())


class BanForeverModal(Modal, title="Вечный бан"):
    description = TextInput(
        label="Причина",
        placeholder="Аргументация",
        default="Вам выдана блокировка на неопределенное вреся в связи с серьёзными нарушениями правил!",
        style=TextStyle.paragraph,
        required=True,
        max_length=512,
    )

    def __init__(self, database, user_to_ban):
        super().__init__()
        self.database = database
        self.user_to_ban = user_to_ban

    async def on_submit(self, interaction) -> None:
        await interaction.response.defer()
        description = self.description.value
        await self.user_to_ban.ban()
        await self.user_to_ban.send(embed=get_user_ban_embed(description))
        await interaction.followup.send(embed=get_user_ban_sent_embed(), ephemeral=True)
