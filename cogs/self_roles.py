""""
Copyright © Krypton 2019-2023 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized discord bot in Python programming language.

Version: 6.1.0
"""

from discord.ext import commands
from discord.ext.commands import Context


# Here we name the cog and create a new class for the cog.
class SelfRoles(commands.Cog, name="self_roles"):
    def __init__(self, bot) -> None:
        self.bot = bot

# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot) -> None:
    await bot.add_cog(SelfRoles(bot))
