from discord.ext import commands
from .embeds.ticket_embed import *
from .views.ticket_views import *
from discord import File
from discord.ext.commands import Context


class Ticket(commands.Cog, name="ticket"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_command(
        name="panel_ticket",
        description="Cоздать панель с созданием жалоб на участников.",
    )
    @commands.has_role("Администратор")
    async def panel_ticket(self, context: Context) -> None:
        await context.defer()
        await context.send("Создание панели...", ephemeral=True)
        await context.send(file=File("src/banners/ticket.png"))
        await context.send(embed=get_ticket_embed(), view=TicketView(self.bot.database))

    async def setup_hook(self) -> None:
        self.add_view(TicketView(self.bot.database))


# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot) -> None:
    await bot.add_cog(Ticket(bot))
