from discord.ext import commands
from discord.utils import get
from .embeds.roles_embed import *
from .views.roles_views import *

# Here we name the cog and create a new class for the cog.
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
        print(member.name)
        for role in join_roles:
            await member.add_roles(get(member.guild.roles, name=role))

    @commands.hybrid_command(
        name="panel_roles",
        with_app_command=True,
        description="Cоздать панель с выбором ролей.",
    )
    @commands.has_role("Администратор")
    async def panel_roles(self, ctx):
        await ctx.defer()
        await ctx.send(roles_banner)
        await ctx.send(valorant_ranking_banner)
        await ctx.send(embed=get_pick_rank_embed(self.bot), view=UserRoleView(self.bot))
        await ctx.send(agent_roles_banner)
        await ctx.send(embed=get_pick_your_agents_embed(self.bot), view=PickAgentsView(self.bot))
        await ctx.send(nick_color_banner)
        await ctx.send(embed=get_pick_your_nick_color_embed(self.bot), view=PickColorView(self.bot))

    async def setup_hook(self) -> None:
        self.add_view(UserRoleView(self.bot))
        self.add_view(PickAgentsView(self.bot))
        self.add_view(PickColorView(self.bot))


async def setup(bot) -> None:
    await bot.add_cog(Roles(bot))
