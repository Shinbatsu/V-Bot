import discord
from discord import app_commands
import datetime
from discord.ext import commands
from discord.ext.commands import Context

class Testing(commands.Cog, name="testing"):
    def __init__(self, bot) -> None:
        self.bot = bot

    async def rps_autocomplete(
        self,
        interaction: discord.Interaction,
        current: str,
    ):
        choices = ["Rock", "Paper", "Scissors"]
        return [app_commands.Choice(name=choice, value=choice) for choice in choices if current.lower() in choice.lower()]

    @commands.hybrid_command(name="rps", description="Limit the number of user(s) in your private channel.")
    @app_commands.autocomplete(choices=rps_autocomplete)
    async def rps(self, interaction: discord.Interaction, choices: str):
        choices = choices.lower()
        if choices == "rock":
            counter = "paper"
        elif choices == "paper":
            counter = "scissors"
        else:
            counter = "rock"
        await interaction.send(f"works, {counter}", ephemeral=True)

# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot) -> None:
    await bot.add_cog(Testing(bot))
