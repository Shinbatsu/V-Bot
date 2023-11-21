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
        self.cooldown = commands.CooldownMapping.from_cooldown(1, 39, commands.BucketType.member)

    @button(
        label="⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀Оставить жалобу на участника⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
        row=0,
        style=ButtonStyle.red,
        custom_id="TicketView:send_report",
    )
    async def send_report(self, interaction, button):
        bucket = self.cooldown.get_bucket(interaction.message)
        retry = bucket.update_rate_limit()
        if retry:
            await interaction.response.defer(ephemeral=True)
            return await interaction.followup.send(
                embed=get_slow_down_embed(round(retry, 1)), ephemeral=True
            )
        await interaction.response.send_modal(
            CreateReportModal(
                self.database,
            )
        )
