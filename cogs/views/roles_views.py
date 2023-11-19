from discord import ButtonStyle, SelectOption
from discord.ui import View, button, select
from discord.utils import get
from ..embeds.roles_embed import *
from ..modals.roles_modals import *
activity_roles = []
rank_roles = [
    "Radiant",
    "Immortal",
    "Ascendant",
    "Diamond",
    "Platinum",
    "Silver",
    "Bronze",
    "Iron",
]
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

class UserRoleView(View):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    @button(label="⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀GET RANK⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀", row=1, style=ButtonStyle.success)
    async def get_rank(self, interaction, button):
        await interaction.response.send_modal(RankModal(self.bot))

    @button(label="⠀⠀⠀⠀⠀UPDATE⠀⠀⠀⠀", row=1, style=ButtonStyle.grey)
    async def update_rank(self, interaction, button):
        valorant_nick_name = await self.bot.database.get_valorant_nickname(interaction.user.id)
        if not valorant_nick_name:
            return await interaction.response.send_message(
                embed=get_cant_update_rank_embed(
                    self.bot,
                ),
                ephemeral=True,
            )
        rank = await fetch_rank(self.rank.value)
        if rank:
            for role in rank_roles:
                await interaction.user.remove_roles(
                    discord.utils.get(interaction.user.guild.roles, name=role)
                )
            await interaction.user.add_roles(
                discord.utils.get(interaction.user.guild.roles, name=rank)
            )
            await interaction.response.send_message(
                embed=get_you_update_rank_embed(
                    self.bot, username=interaction.user.name, rank=rank
                ),
                ephemeral=True,
            )
        else:
            await interaction.response.send_message(
                embed=get_cant_update_rank_embed(self.bot),
                ephemeral=True,
            )


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
            for role in color_roles:
                await interaction.user.remove_roles(get(interaction.user.guild.roles, name=role))
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
