from discord.ext import commands
from discord.ext.commands import Context
import time
from discord import app_commands
class Leveling(commands.Cog, name="leveling"):
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
        is_in_db = await self.bot.database.is_already_exists(member.id)
        if is_in_db:
            return
        await self.bot.database.add_user(member.id)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if not before.channel and after.channel:
            self.data[member.id] = time.time()
        elif before.channel and not after.channel and member.id in self.data:
            new_activity = (time.time() - self.data[member.id]) // 60
            await self.bot.database.update_user_activity(
                user_id=member.id, add_activity=new_activity
            )

async def setup(bot) -> None:
    await bot.add_cog(Leveling(bot))
