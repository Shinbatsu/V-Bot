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

    @commands.command()
    async def sql(self, context: Context):
        await context.defer()
        user_id=383943093310980096
        room_id=711201810110742550
        room =  await self.bot.database.add_user_room(user_id, room_id)
        embed = discord.Embed(
            description=f"**{user_id}** add into the database by **{context.author}**, your personal room is {room}",
            color=0xBEBEFE,
        )
        await context.send(embed=embed)

    @commands.command()
    async def sql2(self, context: Context):
        await context.defer()
        user_id=383943093310980096
        total = await self.bot.database.add_warn(
            user_id, context.guild.id, context.author.id, "Idiot"
        )
        embed = discord.Embed(
            description=f"**{context.author.id}** was warned by **{context.author}**!\nTotal warns for this user: {total}",
            color=0xBEBEFE,
        )
        embed.add_field(name="Reason:", value="Idiot")
        await context.send(embed=embed)
        await context.send(
                f"{context.author.id}, you were warned by **{context.author}**!\nReason:"
            )
    # @commands.Cog.listener()
    # async def on_message_edit(self, before, after):
    #     embed=discord.Embed(title="Message Edited", color=0x00FFFF)
    #     embed.add_field(name='Before:', value=before.content + "u200b", inline=False)
    #     embed.add_field(name="After:", value=after.content + "u200b", inline=False)
    #     channel = self.bot.get_channel(self.bot.config["LOG_CHANNEL_ID"])
    #     await channel.send("DADADAD")

    # @commands.Cog.listener()
    # async def on_message_delete(self, message):
    #     channel = self.bot.get_channel(self.bot.config["LOG_CHANNEL_ID"])
    #     self.bot.logger.info(f"On message delete")
    #     if not message.author.bot:
    #         embed = discord.Embed(
    #             title="Message Deleted",
    #             description=f"{message.author.mention} deleted a message in {message.channel.mention}",
    #             color=discord.Color.red(),
    #         )
    #         embed.add_field(name="Content", value=message.content, inline=False)
    #         embed.set_footer(text=f"User ID: {message.author.id} | Deleted at {discord.utils.utcnow()}")
    #         await channel.send(embed=embed)
# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot) -> None:
    await bot.add_cog(Testing(bot))
