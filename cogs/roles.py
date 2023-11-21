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
    @commands.has_role("Администратор")
    async def panel_roles(self, ctx:Context) -> None:
        self.bot.logger.info("Execute  panel_roles command")
        await ctx.send(file=File("src/banners/roles.png"))
        await ctx.send(file=File("src/banners/valorant_ranking.png"))
        await ctx.send(embed=get_pick_rank_embed(self.bot), view=UserRoleView(self.bot))
        await ctx.send(file=File("src/banners/agent_roles.png"))
        await ctx.send(embed=get_pick_your_agents_embed(self.bot), view=PickAgentsView(self.bot))
        await ctx.send(file=File("src/banners/nick_color.png"))
        await ctx.send(embed=get_pick_your_nick_color_embed(self.bot), view=PickColorView(self.bot))

async def setup(bot) -> None:
    await bot.add_cog(Roles(bot))
