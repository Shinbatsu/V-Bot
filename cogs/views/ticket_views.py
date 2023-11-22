from discord import ButtonStyle
from discord.ext import commands
from discord.ui import View, button
from ..embeds.ticket_embed import *
from ..modals.ticket_modals import *


class TicketView(
    View,
):
    def __init__(self, database):
        self.database = database
        super().__init__(timeout=None)

    @button(
        label="⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀Оставить жалобу на участника⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
        row=0,
        style=ButtonStyle.red,
        custom_id="TicketView:send_report",
    )
    async def send_report(self, interaction, button):
        await interaction.response.send_modal(
            CreateReportModal(
                self.database,
            )
        )
