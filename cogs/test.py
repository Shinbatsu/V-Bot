import discord
from discord import app_commands
import datetime
from discord.ext import commands
from discord.ext.commands import Context

# class MyModal(discord.ui.Modal):
#     def __init__(self, *args, **kwargs) -> None:
#         super().__init__(*args, **kwargs)

#         self.add_item(discord.ui.InputText(label="Short Input"))
#         self.add_item(discord.ui.InputText(label="Long Input", style=discord.InputTextStyle.long))

#     async def callback(self, interaction: discord.Interaction):
#         embed = discord.Embed(title="Modal Results")
#         embed.add_field(name="Short Input", value=self.children[0].value)
#         embed.add_field(name="Long Input", value=self.children[1].value)
#         await interaction.response.send_message(embeds=[embed])


# Here we name the cog and create a new class for the cog.
class Testing(commands.Cog, name="testing"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_command(with_app_command=True)
    async def clear(self, context: Context):
        try:
            await context.channel.purge(limit=100)
        except:
            context.send("Больше нечего удалять!", ephemeral=True)
    async def rps_autocomplete(
        self,
        interaction: discord.Interaction,
        current: str,
    ):
        choices = ["Rock", "Paper", "Scissors"]
        return [app_commands.Choice(name=choice, value=choice) for choice in choices if current.lower() in choice.lower()]

    # If that does not work, try
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
