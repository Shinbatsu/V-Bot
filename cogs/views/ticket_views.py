from discord import ButtonStyle
from discord.ui import View, button
from ..embeds.ticket_embed import *
from ..modals.ticket_modals import *

class TicketView(
    View,
):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    @button(
        label="⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀Оставить жалобу на участника⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
        row=0,
        style=ButtonStyle.red,
    )
    # @commands.cooldown(1, 600, commands.BucketType.user)
    async def send_report(self, interaction, button):
        await interaction.response.send_modal(CreateReportModal(self.bot,))

