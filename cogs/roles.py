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

    # @commands.Cog.listener()
    # async def on_member_join(self, member):
    #     for role in join_roles:
    #         await member.add_roles(get(member.guild.roles, name=role))

    @commands.hybrid_command(
        name="panel_roles",
        description="Create a roles panel.",
    )
    async def _panel_roles(self, context: Context) -> None:
        self.bot.logger.info(str(context.interaction))
        await context.defer(ephemeral=True)
        await context.reply(file=File("src/banners/roles.png"))
        await context.reply(file=File("src/banners/roles.png"))
        await context.send(
            embed=get_pick_your_nick_color_embed(), view=PickColorView(self.bot.database)
        )


async def setup(bot) -> None:
    await bot.add_cog(Roles(bot))
