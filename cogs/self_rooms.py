import discord
from discord.ext import commands, tasks
from discord import ui, PartialEmoji
from discord.ui import View


class SelfRooms(commands.Cog, name="tournaments"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        autoroles = [
            "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀Roles⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
            "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀Agents⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
            "⠀⠀⠀⠀⠀⠀⠀⠀⠀Platform⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
            "⠀⠀⠀⠀⠀⠀⠀⠀Notification⠀⠀⠀⠀⠀⠀⠀⠀⠀",
        ]
        for role in autoroles:
            self.bot.add_roles(member, discord.utils.get(member.guild.roles, name=role))

    @commands.command()
    @commands.has_role("Creator")
    async def room_settings(self, ctx):
        if ctx.channel.id != self.bot.config["ROOM_SETTINGS_CHANNEL_ID"]:
            return
        rooms_settings_embed = discord.Embed(
            title="Управление приватными каналами",
            color=discord.Colour.from_rgb(36, 128, 70),
        )
        rooms_settings_img = discord.Embed(color=discord.Colour.from_rgb(36, 128, 70))
        rooms_settings_img.set_image(
            url="https://cdn.discordapp.com/attachments/1171751170033848360/1173278135119261786/settings_logo.png?ex=65635f69&is=6550ea69&hm=3805968a6ca094a17dae87a60f9c426fce2809ed3ff3db65a30f95f99e3d8675&"
        )
        rooms_settings_embed.add_field(name="<:custom_lock:1173271460970758204> - ```Заблокировать вход в канал```", value="", inline=False)
        rooms_settings_embed.add_field(name="<:kick:1173271463244087336> - ```Исключить пользователя из канала```", value="", inline=False)
        rooms_settings_embed.add_field(
            name="<:slots:1173271467060904050> - ```Изменить количество слотов в канале```", value="", inline=False
        )
        rooms_settings_embed.add_field(name="<:change_owner:1173271455786602526> - ```Изменить владельца канала```", value="", inline=False)
        rooms_settings_embed.add_field(name="<:rename:1173271464699498677> - ```Изменить название канала```", value="", inline=False)
        rooms_settings_embed.add_field(name="CREATE ROOM - ```Создать комнату```", value="", inline=False)
        rooms_settings_embed.set_footer(text="Примечание: Каждый пользователь может иметь только одну комнату!")

        await ctx.message.delete()
        await ctx.send(embed=rooms_settings_img)
        await ctx.send(embed=rooms_settings_embed, view=RoomSettings(self.bot))


# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot) -> None:
    await bot.add_cog(SelfRooms(bot))


class RoomSettings(
    View,
):
    def __init__(self, bot):
        super().__init__()
        self.value = None
        self.bot = bot

    @discord.ui.button(
        label="", emoji=PartialEmoji.from_str("<:custom_lock:1173271460970758204>"), row=0, style=discord.ButtonStyle.secondary
    )
    async def lock(self, interaction, button):
        await interaction.response.send_message("You pressed me!")

    @discord.ui.button(label="", emoji=PartialEmoji.from_str("<:kick:1173271463244087336>"), row=0, style=discord.ButtonStyle.secondary)
    async def kick(self, interaction, button):
        await interaction.response.send_message("You pressed me!")

    @discord.ui.button(label="", emoji=PartialEmoji.from_str("<:slots:1173271467060904050>"), row=0, style=discord.ButtonStyle.secondary)
    async def slots(self, interaction, button):
        await interaction.response.send_message("You pressed me!")

    @discord.ui.button(
        label="", row=0, emoji=PartialEmoji.from_str("<:change_owner:1173271455786602526>"), style=discord.ButtonStyle.secondary
    )
    async def owner(self, interaction, button):
        await interaction.response.send_message("You pressed me!")

    @discord.ui.button(label="", row=0, emoji=PartialEmoji.from_str("<:rename:1173271464699498677>"), style=discord.ButtonStyle.secondary)
    async def rename(self, interaction, button):
        await interaction.response.send_message("You pressed me!")

    @discord.ui.button(label="⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀CREATE ROOM⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀", row=1, style=discord.ButtonStyle.success)
    async def create_room(self, interaction, button):
        await interaction.response.defer()
        current_guild = interaction.guild
        category = await current_guild.create_category(f"{interaction.user.name}'s tournament")
        await current_guild.create_voice_channel(f"Voice", category=category, reason=None, user_limit=5)
