from discord.ext import commands
from discord.ext.commands import Context
from discord import app_commands

# Here we name the cog and create a new class for the cog.
class Template(commands.Cog, name="template"):
    def __init__(self, bot) -> None:
        self.bot = bot

    # Here you can just add your own commands, you'll always need to provide "self" as first parameter.
    async def on_ready(self):
        await self.bot.tree.sync()

    @app_commands.command(
        name="testcommand",
        description="This is a testing command that does nothing.",
    )
    async def testcommand(self, context: Context) -> None:
        """
        This is a testing command that does nothing.

        :param context: The application command context.
        """
        # Do your stuff here

        # Don't forget to remove "pass", I added this just because there's no content in the method.
        pass


# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot) -> None:
    await bot.add_cog(Template(bot))
