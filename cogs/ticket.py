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
    async def panel_ticket(self, ctx: Context) -> None:
        self.bot.logger.info("Execute  panel_ticket command")
        await ctx.send(file=File("src/banners/ticket.png"))
        await ctx.send(embed=get_ticket_embed(self.bot), view=TicketView(self.bot))


# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot) -> None:
    await bot.add_cog(Ticket(bot))
 