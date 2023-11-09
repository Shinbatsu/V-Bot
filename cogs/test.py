""""
Copyright © Krypton 2019-2023 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized discord bot in Python programming language.

Version: 6.1.0
"""
import discord
import datetime
from discord.ext import commands
from discord.ext.commands import Context


class MyView(discord.ui.View): # Create a class called MyView that subclasses discord.ui.View
    @discord.ui.button(label="Click me!", style=discord.ButtonStyle.primary, emoji="😎") # Create a button with the label "😎 Click me!" with color Blurple
    async def button_callback(self, interaction, button ):
        await interaction.response.send_message("You clicked the button!") # Send a message when the button is clicked



# Here we name the cog and create a new class for the cog.
class Testing(commands.Cog, name="testing"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_command() # Create a slash command
    async def button(self, ctx):
        await ctx.send("Wow! It works!", view=MyView()) # Send a message with our View class that contains the button

    # Here you can just add your own commands, you'll always need to provide "self" as first parameter.
    @commands.command()
    # pycord will figure out the types for you
    async def add(self, ctx, first: int, second: int):
        # you can use them as they were actual integers
        sum = first + second
        await ctx.reply(f"The sum of {first} and {second} is {sum}.")

    @commands.hybrid_command()
    async def tests(self, ctx: Context) -> None:
        embed = discord.Embed(
            title="My Amazing Embed",
            description="Embeds are super easy, barely an inconvenience.",
            color=discord.Colour.blurple(), # Pycord provides a class with default colors you can choose from
        )
        embed.add_field(name="A Normal Field", value="A really nice field with some information. **The description as well as the fields support markdown!**")

        embed.add_field(name="Inline Field 1", value="Inline Field 1", inline=True)
        embed.add_field(name="Inline Field 2", value="Inline Field 2", inline=True)
        embed.add_field(name="Inline Field 3", value="Inline Field 3", inline=True)
    
        embed.set_footer(text="Footer! No markdown here.") # footers can have icons too
        embed.set_author(name="Pycord Team", icon_url="https://cybersport.metaratings.ru/storage/images/4f/9a/4f9ab43ff49dd6ad63eaf036295f12cb.jpg")
        embed.set_thumbnail(url="https://cybersport.metaratings.ru/storage/images/4f/9a/4f9ab43ff49dd6ad63eaf036295f12cb.jpg")
        embed.set_image(url="https://cybersport.metaratings.ru/storage/images/4f/9a/4f9ab43ff49dd6ad63eaf036295f12cb.jpg")
    
        await ctx.send("Hello! Here's a cool embed.", embed=embed) # Send the embed with some text


# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot) -> None:
    await bot.add_cog(Testing(bot))
