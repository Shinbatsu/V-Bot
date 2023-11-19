from discord import ButtonStyle
from discord.ext import commands
from discord.ui import View, button
from ..embeds.ticket_embed import *
from ..modals.ticket_modals import *


class TicketView(
    View,
):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot
        self.cooldown = commands.CooldownMapping.from_cooldown(1, 39, commands.BucketType.member)

    @button(
        label="⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀Оставить жалобу на участника⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
        row=0,
        style=ButtonStyle.red,
        custom_id="TicketView:send_report",
    )
    async def send_report(self, interaction, button):
        await interaction.defer()
        bucket = self.cooldown.get_bucket(interaction.message)
        retry = bucket.update_rate_limit()
        if retry:
            return await interaction.followup.send_message(
                embed=get_slow_down_embed(self.bot, round(retry, 1)), ephemeral=True
            )
        await interaction.followup.send_modal(
            CreateReportModal(
                self.bot,
            )
        )
