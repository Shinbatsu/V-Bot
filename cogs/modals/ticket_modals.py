from discord import TextStyle
from discord.ui import TextInput, Modal, button
from discord.utils import get
from ..embeds.ticket_embed import *


class CreateReportModal(Modal, title="Создание жалобы"):
    reported_user = TextInput(
        label="Введите ID или ник пользователя",
        placeholder="@shinbatsuf | 383943093310980096",
        default="",
        style=TextStyle.short,
        required=True,
        max_length=50,
    )
    description = TextInput(
        label="Введите ID или ник пользователя",
        placeholder="Подробно опишите причину...",
        default="",
        style=TextStyle.paragraph,
        required=True,
        max_length=512,
    )

    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    async def on_submit(self, interaction) -> None:
        report_channel = self.bot.get_channel(id=self.bot.config["REPORT_CHANNEL_ID"])
        reported_user = str(self.reported_user.value)
        description = self.description.value
        report_channel.send(
            embed=get_report_info_embed(self.bot, interaction.user.name, reported_user, description)
        )
        await interaction.response.send_message(
            embed=get_report_sent_embed(self.bot), ephemeral=True
        )
