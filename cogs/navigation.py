from discord.ext import commands
from .embeds.navigation_embed import *
from .views.navigation_views import *
from discord.ext.commands import Context

# from .views.navigation_views import *
from discord import File



# Here we name the cog and create a new class for the cog.
class Navigation(commands.Cog, name="navigation"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_command(
        name="panel_navigation",
        description="Cоздать панель с навигационными кнопками.",
    )
    async def _panel_navigation(self, context: Context) -> None:
        self.bot.logger.info(type(context))
        await context.send("Создание панели...", ephemeral=True)
        await context.send(file=File("src/banners/navigation.png"))
        await context.send(
            embed=get_navigation_room_embed(),
            view=NavigationView(),
        )
    async def setup_hook(self) -> None:
        self.add_view(NavigationView())

# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot) -> None:
    await bot.add_cog(Navigation(bot))
