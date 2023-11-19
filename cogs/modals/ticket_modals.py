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

    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.guild = self.bot.get_guild(self.bot.config["GUILD_ID"])
        

    def get_member_by_name(self, username):
        for member in self.guild.members:
            if member.name == username:
                return member

    async def on_submit(self, interaction) -> None:
        await interaction.defer()
        if self.reported_user.value.isdigit():
            self.reported_user = self.guild.get_member(int(self.reported_user.value))
        else:
            self.reported_user = self.get_member_by_name(self.reported_user.value)
        if self.reported_user.id == interaction.user.id:
            await interaction.followup.send_message(
                embed=get_report_sent_embed(self.bot), ephemeral=True
            )
        report_channel = self.bot.get_channel(self.bot.config["REPORT_CHANNEL_ID"])
        description = self.description.value
        message = await report_channel.send(".")
        message_url = message.jump_url
        await message.edit(
            embed=get_report_info_embed(
                self.bot, interaction.user.name, self.reported_user.name, description
            ),
            view=ModeratorActionView(self.bot, self.reported_user, message_url),
        )
        await interaction.followup.send_message(
            embed=get_report_sent_embed(self.bot), ephemeral=True
        )


class ModeratorActionView(View):
    def __init__(self, bot, user_to_action, message_url):
        super().__init__()
        self.bot = bot
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
        await interaction.defer()
        user_pick = select.values[0]
        if user_pick == "Закрыть жалобу":
            self.action.disabled = True
            await interaction.followup.send_message(
                embed=get_report_was_resolved_embed(
                    self.bot, self.message_url, interaction.user.name
                )
            )
        elif user_pick == "Отправить предупреждение":
            await interaction.followup.send_modal(UserWarnModal(self.bot, self.user_to_action))
        elif user_pick == "Кик":
            await interaction.followup.send_modal(UserKickModal(self.bot, self.user_to_action))
        elif user_pick == "Временный мут":
            await interaction.followup.send_modal(TempMuteModal(self.bot, self.user_to_action))
        elif user_pick == "Временный запрет печати":
            await interaction.followup.send_modal(
                TempStopTypingModal(self.bot, self.user_to_action)
            )
        elif user_pick == "Временный бан":
            await interaction.followup.send_modal(TempBanModal(self.bot, self.user_to_action))
        elif user_pick == "Бан-хаммер":
            await interaction.followup.send_modal(BanForeverModal(self.bot, self.user_to_action))


class UserWarnModal(Modal, title="Замечание"):
    description = TextInput(
        label="Причина",
        placeholder="Аргументация",
        default="Вам выдано замечание в связи с жалобами!",
        style=TextStyle.paragraph,
        required=True,
        max_length=512,
    )

    def __init__(self, bot, user_to_warn):
        super().__init__()
        self.bot = bot
        self.user_to_warn = user_to_warn

    async def on_submit(self, interaction) -> None:
        description = self.description.value
        await self.user_to_warn.send(embed=get_user_warn_embed(self.bot, description))
        await interaction.followup.send_message(
            embed=get_user_warn_sent_embed(self.bot), ephemeral=True
        )


class UserKickModal(Modal, title="Кик"):
    description = TextInput(
        label="Причина",
        placeholder="Аргументация",
        default="Вас кикнули с сервера в связи с жалобами!",
        style=TextStyle.paragraph,
        required=True,
        max_length=512,
    )

    def __init__(self, bot, user_to_kick):
        super().__init__()
        self.bot = bot
        self.user_to_kick = user_to_kick

    async def on_submit(self, interaction) -> None:
        await interaction.defer() 
        description = self.description.value
        await self.user_to_kick.send(embed=get_user_kick_embed(self.bot, description))
        await interaction.followup.send_message(
            embed=get_user_kick_sent_embed(self.bot), ephemeral=True
        )


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

    def __init__(self, bot, user_to_mute):
        super().__init__()
        self.bot = bot
        self.guild = self.bot.get_guild(self.bot.config["GUILD_ID"])
        self.user_to_mute = self.guild.get_member(user_to_mute.id)

    async def on_submit(self, interaction) -> None:
        await interaction.defer() 
        description = self.description.value
        mute_role = [*filter(lambda role: role.name == "M", self.guild.roles)][0]
        await self.user_to_mute.add_roles(mute_role)
        time = int(self.seconds.value)
        await self.user_to_mute.send(embed=get_user_temp_mute_embed(self.bot, description, time))
        await interaction.followup.send_message(
            embed=get_user_temp_mute_sent_embed(self.bot), ephemeral=True
        )
        await asyncio.sleep(time)
        await self.user_to_mute.remove_roles(mute_role)
        await self.user_to_mute.send(embed=get_user_unmute_embed(self.bot))


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

    def __init__(self, bot, user_to_stop_typing):
        super().__init__()
        self.bot = bot
        self.guild = self.bot.get_guild(self.bot.config["GUILD_ID"])
        self.user_to_stop_typing = self.guild.get_member(user_to_stop_typing.id)

    async def on_submit(self, interaction) -> None:
        await interaction.defer() 
        description = self.description.value
        stop_typing_role = [*filter(lambda role: role.name == "T", self.guild.roles)][0]
        await self.user_to_stop_typing.add_roles(stop_typing_role)
        time = int(self.seconds.value)
        await self.user_to_stop_typing.send(
            embed=get_user_temp_stop_typing_embed(self.bot, description, time)
        )
        await interaction.followup.send_message(
            embed=get_user_temp_stop_typing_sent_embed(self.bot), ephemeral=True
        )
        await asyncio.sleep(time)
        await self.user_to_stop_typing.remove_roles(stop_typing_role)
        await self.user_to_stop_typing.send(embed=get_user_temp_unstop_typing_embed(self.bot))


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

    def __init__(self, bot, user_to_ban):
        super().__init__()
        self.bot = bot
        self.guild = self.bot.get_guild(self.bot.config["GUILD_ID"])
        self.user_to_ban = self.guild.get_member(user_to_ban.id)

    async def on_submit(self, interaction) -> None:
        await interaction.defer()
        description = self.description.value
        temp_ban_role = [*filter(lambda role: role.name == "B", self.guild.roles)][0]
        await self.user_to_ban.add_roles(temp_ban_role)
        time = int(self.seconds.value)
        await self.user_to_ban.send(
            embed=get_user_temp_stop_typing_embed(self.bot, description, time)
        )
        lp_room = self.bot.get_channel(self.bot.config["SHIT"])
        await self.user_to_ban.edit(voice_channel=lp_room)
        await interaction.followup.send_message(
            embed=get_user_temp_ban_sent_embed(self.bot), ephemeral=True
        )
        await asyncio.sleep(time)
        await self.user_to_ban.remove_roles(temp_ban_role)
        await self.user_to_ban.send(embed=get_user_unban_embed(self.bot))


class BanForeverModal(Modal, title="Вечный бан"):
    description = TextInput(
        label="Причина",
        placeholder="Аргументация",
        default="Вам выдана блокировка на неопределенное вреся в связи с серьёзными нарушениями правил!",
        style=TextStyle.paragraph,
        required=True,
        max_length=512,
    )

    def __init__(self, bot, user_to_ban):
        super().__init__()
        self.bot = bot
        self.user_to_ban = user_to_ban

    async def on_submit(self, interaction) -> None:
        await interaction.defer()
        description = self.description.value
        await self.user_to_ban.send(embed=get_user_ban_embed(self.bot, description))
        await interaction.followup.send_message(
            embed=get_user_ban_sent_embed(self.bot), ephemeral=True
        )
