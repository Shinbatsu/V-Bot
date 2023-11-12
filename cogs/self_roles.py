from discord.ext import commands
from discord.ext.commands import Context
from discord.app_commands import Choice
from typing import Literal
from discord import app_commands
import discord


# Here we name the cog and create a new class for the cog.
class SelfRoles(commands.Cog, name="self_roles"):
    def __init__(self, bot) -> None:
        self.bot = bot

    async def rps_autocomplete(self,
        interaction: discord.Interaction,
        current: str,
    ):
        choices = ['Rock', 'Paper', 'Scissors']
        return [
            app_commands.Choice(name=choice, value=choice)
            for choice in choices if current.lower() in choice.lower()
        ]
    # If that does not work, try
    @commands.hybrid_command(name="rps", description="Limit the number of user(s) in your private channel.")
    @app_commands.autocomplete(choices=rps_autocomplete)
    async def rps(self, interaction: discord.Interaction, choices:str):
        choices = choices.lower()
        if (choices == 'rock'):
            counter = 'paper'
        elif (choices == 'paper'):
            counter = 'scissors'
        else:
            counter = 'rock'
        await interaction.send(f"works, {counter}", ephemeral=True)

    # @commands.command()
    # @commands.describe(fruits='Fruits to choose from')
    # async def fruit(ctx, fruits: str):
    #     valid_fruits = ['apple', 'banana', 'cherry']

    #     if fruits.lower() in valid_fruits:
    #         await ctx.send(f'Your favorite fruit is {fruits}.')
    #     else:
    #         await ctx.send('Invalid fruit choice. Please choose from apple, banana, or cherry.')


# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot) -> None:
    await bot.add_cog(SelfRoles(bot))
