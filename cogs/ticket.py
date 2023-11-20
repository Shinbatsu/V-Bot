from discord.ext import commands
from .embeds.ticket_embed import *
from .views.ticket_views import *
from discord import app_commands

class Ticket(commands.Cog, name="ticket"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @app_commands.command(
        name="panel_ticket",
        with_app_command=True,
        description="Cоздать панель с созданием жалоб на участников.",
    )
    @commands.has_role("Администратор")
    async def panel_ticket(self, ctx):
        await ctx.defer()
        await ctx.send(ticket_banner)
        await ctx.send(embed=get_ticket_embed(self.bot), view=TicketView(self.bot))

    async def on_ready(self):
        await self.bot.tree.sync()

    async def setup_hook(self) -> None:
        self.add_view(TicketView(self.bot))


# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot) -> None:
    await bot.add_cog(Ticket(bot))
