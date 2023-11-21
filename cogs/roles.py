from discord.ext import commands
from discord.utils import get
from .embeds.roles_embed import *
from .views.roles_views import *
from discord import File
from discord.ext.commands import Context
join_roles = [
    "⠀⠀⠀⠀⠀⠀⠀⠀⠀AGENTS⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
    "⠀⠀⠀⠀⠀⠀⠀NOTIFICATION⠀⠀⠀⠀⠀⠀⠀⠀",
    "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀RANK⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
    "Member",
]


class Roles(commands.Cog, name="roles"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        for role in join_roles:
            await member.add_roles(get(member.guild.roles, name=role))
    @commands.hybrid_command(
        name="panel_roles",
        description="Cоздать панель с выбором ролей.",
    )
    async def _panel_roles(self, context:Context) -> None:
        self.bot.logger.info(type(context))
        await context.reply("Создание панели...", ephemeral=True)
        await context.reply(file=File("src/banners/roles.png"))
        await context.reply(file=File("src/banners/valorant_ranking.png"))
        await context.reply(embed=get_pick_rank_embed(), view=PickRankView(self.bot.database))
        await context.reply(file=File("src/banners/agent_roles.png"))
        await context.reply(embed=get_pick_your_agents_embed(), view=PickAgentsView(self.bot.database))
        await context.reply(file=File("src/banners/nick_color.png"))
        await context.reply(embed=get_pick_your_nick_color_embed(), view=PickColorView(self.bot.database))
    
    async def setup_hook(self) -> None:
        self.add_view(PickRankView(self.bot.database))
        self.add_view(PickAgentsView(self.bot.database))
        self.add_view(PickColorView(self.bot.database))

async def setup(bot) -> None:
    await bot.add_cog(Roles(bot))
