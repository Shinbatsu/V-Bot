from discord import ButtonStyle, SelectOption
from discord.ui import View, button, select
from discord.utils import get
from discord.ext import commands
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


class PickRankView(View):
    def __init__(self, database):
        super().__init__(timeout=None)
        self.database = database
        self.cooldown = commands.CooldownMapping.from_cooldown(1, 39, commands.BucketType.member)

    @button(
        label="⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀GET RANK⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
        row=1,
        style=ButtonStyle.success,
        custom_id="PickRankView:get_rank",
    )
    async def get_rank(self, interaction, button):
        await interaction.response.send_modal(RankModal(self.database))

    @button(
        label="⠀⠀⠀⠀⠀UPDATE⠀⠀⠀⠀",
        row=1,
        style=ButtonStyle.grey,
        custom_id="PickRankView:update_rank",
    )
    async def update_rank(self, interaction, button):
        await interaction.response.defer(ephemeral=True)
        valorant_nick_name = await self.database.get_valorant_nickname(interaction.user.id)
        if not valorant_nick_name:
            return await interaction.followup.send(
                embed=get_cant_update_rank_embed(),
                ephemeral=True,
            )
        rank = await fetch_rank(valorant_nick_name)
        if rank:
            for role in rank_roles:
                await interaction.user.remove_roles(
                    discord.utils.get(interaction.user.guild.roles, name=role)
                )
            await interaction.user.add_roles(
                discord.utils.get(interaction.user.guild.roles, name=rank)
            )
            await interaction.followup.send(
                embed=get_you_update_rank_embed(username=interaction.user.name, rank=rank),
                ephemeral=True,
            )
        else:
            await interaction.followup.send(
                embed=get_cant_update_rank_embed(),
                ephemeral=True,
            )


class PickColorView(View):
    def __init__(self, database):
        super().__init__(timeout=None)
        self.database = database

    async def on_timeout(self):
        print("TIMEOUT")

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
            SelectOption(label="Убрать"),
        ],
        custom_id="PickColorView:color",
    )
    async def color(self, interaction, select):
        await interaction.response.defer(ephemeral=True)
        color_roles_o = [*filter(lambda x: x.name in color_roles, interaction.guild.roles)]
        user_roles = [role.name for role in interaction.user.roles]
        user_pick = select.values[0]
        if user_pick in user_roles or user_pick == "Убрать":
            await interaction.user.remove_roles(*color_roles_o)
            await interaction.followup.send(embed=get_color_nick_removed_embed(), ephemeral=True)
        else:
            await interaction.user.remove_roles(*color_roles_o)
            for role in color_roles_o:
                if role.name == user_pick:
                    await interaction.user.add_roles(role)
            await interaction.followup.send(embed=get_color_nick_added_embed(), ephemeral=True)

class PickAgentsView(View):
    def __init__(self, database):
        super().__init__(timeout=None)
        self.database = database

    @select(
        placeholder="Стражи",
        min_values=1,
        max_values=1,
        options=[*[SelectOption(label=x) for x in guardian_roles], SelectOption(label="Убрать")],
        custom_id="PickAgentsView:guardians_callback",
    )
    async def guardians_callback(self, interaction, select):
        await interaction.response.defer(ephemeral=True)
        guardian_roles_o = [*filter(lambda x: x.name in guardian_roles, interaction.guild.roles)]
        user_roles = [role.name for role in interaction.user.roles]
        user_pick = select.values[0]
        if user_pick in user_roles or user_pick == "Убрать":
            await interaction.user.remove_roles(*guardian_roles_o)
            await interaction.followup.send(embed=get_agent_removed_embed(), ephemeral=True)
        else:
            for role in guardian_roles_o:
                if role.name == user_pick:
                    await interaction.user.add_roles(role)
            await interaction.followup.send(embed=get_agent_added_embed(), ephemeral=True)

    @select(
        placeholder="Дуэлянты",
        min_values=1,
        max_values=1,
        options=[*[SelectOption(label=x) for x in duelist_roles], SelectOption(label="Убрать")],
        custom_id="PickAgentsView:duelist_callback",
    )
    async def duelist_callback(self, interaction, select):
        await interaction.response.defer(ephemeral=True)
        duelist_roles_o = [*filter(lambda x: x.name in duelist_roles, interaction.guild.roles)]
        user_roles = [role.name for role in interaction.user.roles]
        user_pick = select.values[0]
        if user_pick in user_roles or user_pick == "Убрать":
            await interaction.user.remove_roles(*duelist_roles_o)
            await interaction.followup.send(embed=get_agent_removed_embed(), ephemeral=True)
        else:
            for role in duelist_roles_o:
                if role.name == user_pick:
                    await interaction.user.add_roles(role)
            await interaction.followup.send(embed=get_agent_added_embed(), ephemeral=True)
    @select(
        placeholder="Зачинщики",
        min_values=1,
        max_values=1,
        options=[*[SelectOption(label=x) for x in initiator_roles], SelectOption(label="Убрать")],
        custom_id="PickAgentsView:initiator_callback",
    )
    async def initiator_callback(self, interaction, select):
        await interaction.response.defer(ephemeral=True)
        initiator_roles_o = [*filter(lambda x: x.name in initiator_roles, interaction.guild.roles)]
        user_roles = [role.name for role in interaction.user.roles]
        user_pick = select.values[0]
        if user_pick in user_roles or user_pick == "Убрать":
            await interaction.user.remove_roles(*initiator_roles_o)
            await interaction.followup.send(embed=get_agent_removed_embed(), ephemeral=True)
        else:
            for role in initiator_roles_o:
                if role.name == user_pick:
                    await interaction.user.add_roles(role)
            await interaction.followup.send(embed=get_agent_added_embed(), ephemeral=True)

    @select(
        placeholder="Специалисты",
        min_values=1,
        max_values=1,
        options=[*[SelectOption(label=x) for x in specialist_roles], SelectOption(label="Убрать")],
        custom_id="PickAgentsView:specialist_callback",
    )
    async def specialist_callback(self, interaction, select):
        await interaction.response.defer(ephemeral=True)
        specialist_roles_o = [*filter(lambda x: x.name in specialist_roles, interaction.guild.roles)]
        user_roles = [role.name for role in interaction.user.roles]
        user_pick = select.values[0]
        if user_pick in user_roles or user_pick == "Убрать":
            await interaction.user.remove_roles(*specialist_roles_o)
            await interaction.followup.send(embed=get_agent_removed_embed(), ephemeral=True)
        else:
            for role in specialist_roles_o:
                if role.name == user_pick:
                    await interaction.user.add_roles(role)
            await interaction.followup.send(embed=get_agent_added_embed(), ephemeral=True)
