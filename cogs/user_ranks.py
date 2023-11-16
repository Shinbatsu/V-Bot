from discord.ext import commands
from discord.ext.commands import Context
import time


# Here we name the cog and create a new class for the cog.
class UserRanks(commands.Cog, name="user_ranks"):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.data = {}

    @commands.Cog.listener()
    async def on_ready(self):
        guild = self.bot.get_guild(self.bot.config["GUILD_ID"])
        user_ids = await self.bot.database.get_all_user_ids()
        member_ids = [member.id for member in guild.members]
        for id in member_ids:
            if id not in user_ids:
                await self.bot.database.add_user(id)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await self.bot.database.add_user(member.id)

    @commands.hybrid_command(with_app_command=True)
    async def add_user_in_db(self, ctx, user_id: int):
        await self.bot.database.add_user(user_id)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if not before.channel and after.channel:
            self.data[member.id] = time.time()
        elif before.channel and not after.channel and member.id in self.data:
            new_activity = (time.time() - self.data[member.id]) // 60
            await self.bot.database.updata_acitivity(user_id=member.id, add_activity=new_activity)

    @commands.command()
    async def profile(self, ctx):
        await ctx.send(ctx.author.avatar.url)
    

# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot) -> None:
    await bot.add_cog(UserRanks(bot))
