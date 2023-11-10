import discord
from discord.ext import commands, tasks
from discord import ui
from ui_components import tournament_announcement


@tasks.loop(minutes=1)
async def test():
    channel = client.get_channel(CHANNEL_ID)
    await channel.send("test")


class Tournaments(commands.Cog, name="tournaments"):
    def __init__(self, bot) -> None:
        self.bot = bot

    # Here you can just add your own commands, you'll always need to provide "self" as first parameter.
    @tasks.loop()
    @commands.hybrid_command(
        name="create_room",
        description="This is a command that creates tournament room.",
    )
    async def create_room(self, ctx, tournament_name="", player_limit=5):
        try:
            current_guild_id = ctx.channel.id
            if current_guild_id == self.bot.config["TOURNAMENT_CHANNEL_ID"]:
                await ctx.send("Tournament!")
                author_name = ctx.author.name  # Get the author's name
                category_name = tournament_name or author_name
                guild = ctx.message.guild
                await ctx.send("Setting up tournament...")
                category = await guild.create_category(f"{category_name}'s tournament")

                await guild.create_voice_channel(f"Voice", category=category, reason=None, user_limit=5)
                await ctx.send("Tournament room created!")

        except Exception as e:
            print(f"what? {e}")


# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot) -> None:
    await bot.add_cog(Tournaments(bot))
