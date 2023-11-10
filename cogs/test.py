""""
Copyright © Krypton 2019-2023 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized discord bot in Python programming language.

Version: 6.1.0
"""
import discord
from discord import app_commands
import datetime
from discord.ext import commands
from discord.ext.commands import Context


class MyView(discord.ui.View):  # Create a class called MyView that subclasses discord.ui.View
    @discord.ui.button(label="Click me!", style=discord.ButtonStyle.primary)
    async def button_callback(self, interaction, button):
        await interaction.response.send_message("You clicked the button!")  # Send a message when the button is clicked


class MyModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="Short Input"))
        self.add_item(discord.ui.InputText(label="Long Input", style=discord.InputTextStyle.long))

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Modal Results")
        embed.add_field(name="Short Input", value=self.children[0].value)
        embed.add_field(name="Long Input", value=self.children[1].value)
        await interaction.response.send_message(embeds=[embed])


# Here we name the cog and create a new class for the cog.
class Testing(commands.Cog, name="testing"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_command()
    async def modal_slash(self, ctx: Context):
        """Shows an example of a modal dialog being invoked from a slash command."""
        modal = MyModal(title="Modal via Slash Command")
        await ctx.send_modal(modal)

    @commands.hybrid_command(name="button", description="This is a testing command that does nothing.", with_app_command=True)
    async def button(self, ctx):
        await ctx.send("Wow! It works!", view=MyView())  # Send a message with our View class that contains the button

    # Here you can just add your own commands, you'll always need to provide "self" as first parameter.
    @commands.hybrid_command(name="add", description="This is a testing command that does nothing.", with_app_command=True)
    async def add(self, ctx, first: int, second: int):
        # you can use them as they were actual integers
        sum = first + second
        await ctx.reply(f"The sum of {first} and {second} is {sum}.")


# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot) -> None:
    await bot.add_cog(Testing(bot))
