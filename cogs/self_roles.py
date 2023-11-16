from discord.ext import commands
from discord import ui, PartialEmoji, ButtonStyle, PermissionOverwrite, SelectOption
from discord.ui import View, button, select, Select
from discord.utils import get
from .embeds.self_roles_embed import *

# from .modals.self_roles_embed import *
from discord import PermissionOverwrite

# Here we name the cog and create a new class for the cog.
join_roles = [
    "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀Roles⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
    "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀Agents⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
    "⠀⠀⠀⠀⠀⠀⠀⠀Notification⠀⠀⠀⠀⠀⠀⠀⠀⠀",
    "Member",
]
activity_roles = []

color_roles = [
    "Red",
    "Yellow",
    "Black",
    "Orange",
    "Green",
]

guardian_roles = [
    "Killjoy",
    "Cypher",
    "Sage",
    "Chamber",
]
duelist_roles = [
    "Phoenix",
    "Jett",
    "Reyna",
    "Raze",
    "Yoru",
    "Neon",
    "ISO",
]
initiator_roles = [
    "Sova",
    "Breach",
    "Skye",
    "Kayo",
    "Fade",
    "Gekko",
    "KAY/O",
]
specialist_roles = [
    "Brimstone",
    "Omen",
    "Viper",
    "Astra",
    "Harbor",
]


class SelfRoles(commands.Cog, name="self_roles"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        for role in join_roles:
            await member.add_roles(get(member.guild.roles, name=role))

    @commands.command()
    @commands.has_role("Creator")
    async def agent_roles_panel(self, ctx):
        if ctx.channel.id != self.bot.config["ROLES_ROOM_CHANNEL_ID"]:
            return
        await ctx.message.delete()
        await ctx.send(agent_roles_banner)
        await ctx.send(embed=get_pick_your_agents_embed(self.bot), view=PickAgentsView(self.bot))

    @commands.command()
    @commands.has_role("Creator")
    async def nick_color_panel(self, ctx):
        if ctx.channel.id != self.bot.config["ROLES_ROOM_CHANNEL_ID"]:
            return
        await ctx.message.delete()
        await ctx.send(nick_color_banner)
        await ctx.send(embed=get_pick_your_nick_color_embed(self.bot), view=PickColorView(self.bot))


class PickColorView(View):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    @select(
        placeholder="Выбери цвет",
        min_values=1,
        max_values=1,
        options=[
            SelectOption(label="Red"),
            SelectOption(label="Green"),
            SelectOption(label="Yellow"),
            SelectOption(label="Black"),
            SelectOption(label="Orange"),
            SelectOption(label="Remove"),
        ],
    )
    async def callback(self, interaction, select):
        user_pick = select.values[0]
        user_roles = [role.name for role in interaction.user.roles]
        if user_pick in user_roles or user_pick == "Remove":
            await interaction.user.remove_roles(get(interaction.user.guild.roles, name=user_pick))
            await interaction.response.send_message(
                embed=get_color_nick_removed_embed(self.bot), ephemeral=True
            )
        elif any([x in color_roles for x in user_roles]):
            await interaction.response.send_message(
                embed=get_color_already_selected_embed(self.bot), ephemeral=True
            )
        elif user_pick != "Remove":
            await interaction.user.add_roles(get(interaction.user.guild.roles, name=user_pick))
            await interaction.response.send_message(
                embed=get_color_nick_added_embed(self.bot), ephemeral=True
            )
        else:
            await interaction.response.send_message(
                embed=get_no_color_to_remove_embed(self.bot), ephemeral=True
            )


class PickAgentsView(View):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    @select(
        placeholder="Стражи",
        min_values=1,
        max_values=1,
        options=[SelectOption(label=x) for x in guardian_roles],
    )
    async def guardians_callback(self, interaction, select):
        user_roles = [role.name for role in interaction.user.roles]
        user_pick = select.values[0]
        if user_pick in user_roles:
            await interaction.user.remove_roles(get(interaction.user.guild.roles, name=user_pick))
            await interaction.response.send_message(
                embed=get_agent_removed_embed(self.bot), ephemeral=True
            )
        elif any([x in guardian_roles for x in user_roles]):
            await interaction.response.send_message(
                embed=get_agent_already_selected_embed(self.bot), ephemeral=True
            )
        else:
            await interaction.user.add_roles(get(interaction.user.guild.roles, name=user_pick))
            await interaction.response.send_message(
                embed=get_agent_added_embed(self.bot), ephemeral=True
            )

    @select(
        placeholder="Дуэлянты",
        min_values=1,
        max_values=1,
        options=[SelectOption(label=x) for x in duelist_roles],
    )
    async def duelist_callback(self, interaction, select):
        user_roles = [role.name for role in interaction.user.roles]
        user_pick = select.values[0]
        if user_pick in user_roles:
            await interaction.user.remove_roles(get(interaction.user.guild.roles, name=user_pick))
            await interaction.response.send_message(
                embed=get_agent_removed_embed(self.bot), ephemeral=True
            )
        elif any([x in duelist_roles for x in user_roles]):
            await interaction.response.send_message(
                embed=get_agent_already_selected_embed(self.bot), ephemeral=True
            )
        else:
            await interaction.user.add_roles(get(interaction.user.guild.roles, name=user_pick))
            await interaction.response.send_message(
                embed=get_agent_added_embed(self.bot), ephemeral=True
            )

    @select(
        placeholder="Зачинщики",
        min_values=1,
        max_values=1,
        options=[SelectOption(label=x) for x in initiator_roles],
    )
    async def initiator_callback(self, interaction, select):
        user_roles = [role.name for role in interaction.user.roles]
        user_pick = select.values[0]
        if user_pick in user_roles:
            await interaction.user.remove_roles(get(interaction.user.guild.roles, name=user_pick))
            await interaction.response.send_message(
                embed=get_agent_removed_embed(self.bot), ephemeral=True
            )
        elif any([x in initiator_roles for x in user_roles]):
            await interaction.response.send_message(
                embed=get_agent_already_selected_embed(self.bot), ephemeral=True
            )
        else:
            await interaction.user.add_roles(get(interaction.user.guild.roles, name=user_pick))
            await interaction.response.send_message(
                embed=get_agent_added_embed(self.bot), ephemeral=True
            )

    @select(
        placeholder="Специалисты",
        min_values=1,
        max_values=1,
        options=[SelectOption(label=x) for x in specialist_roles],
    )
    async def specialist_callback(self, interaction, select):
        user_roles = [role.name for role in interaction.user.roles]
        user_pick = select.values[0]
        if user_pick in user_roles:
            await interaction.user.remove_roles(get(interaction.user.guild.roles, name=user_pick))
            await interaction.response.send_message(
                embed=get_agent_removed_embed(self.bot), ephemeral=True
            )
        elif any([x in specialist_roles for x in user_roles]):
            await interaction.response.send_message(
                embed=get_agent_already_selected_embed(self.bot), ephemeral=True
            )
        else:
            await interaction.user.add_roles(get(interaction.user.guild.roles, name=user_pick))
            await interaction.response.send_message(
                embed=get_agent_added_embed(self.bot), ephemeral=True
            )


async def setup(bot) -> None:
    await bot.add_cog(SelfRoles(bot))
