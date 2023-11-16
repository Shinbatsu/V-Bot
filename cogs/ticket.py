from discord.ext import commands
from discord import ui, PartialEmoji, ButtonStyle, PermissionOverwrite
from discord.ui import View, button, Button
from discord.utils import get
from .embeds.ticket_embed import *
from .modals.ticket_modals import *
from discord import PermissionOverwrite


class NavigationView(
    View,
):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    @button(
        label="",
        row=0,
        emoji=PartialEmoji.from_str("<:change_owner:1173271455786602526>"),
        style=ButtonStyle.secondary,
    )
    @commands.cooldown(1, 600, commands.BucketType.user)
    async def send_report(self, interaction, button):
        await interaction.response.send_modal(CreateReportModal(self.bot))


class Ticket(commands.Cog, name="ticket"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command()
    async def ticket_panel(self, ctx):
        await ctx.send(ticket_banner)
        await ctx.send(embed=get_ticket_embed(self.bot))


# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot) -> None:
    await bot.add_cog(Ticket(bot))
