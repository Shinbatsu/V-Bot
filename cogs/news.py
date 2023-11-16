from discord.ext import commands
from discord.ext.commands import Context


# Here we name the cog and create a new class for the cog.
class News(commands.Cog, name="news"):
    def __init__(self, bot) -> None:
        self.bot = bot


# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot) -> None:
    await bot.add_cog(News(bot))
