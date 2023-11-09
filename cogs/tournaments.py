import discord
from discord.ext import commands
from discord import ui

class Tournaments(commands.Cog, name="tournaments"):
    def __init__(self, bot) -> None:
        self.bot = bot

    # Here you can just add your own commands, you'll always need to provide "self" as first parameter.

    @commands.hybrid_command(
        name="tournament",
        description="This is a testing command that does nothing.",
    )
    @commands.has_role("Creator")
    async def tournament(self, ctx, tournament_name=""):
        try:
            current_guild_id = ctx.channel.id
            if current_guild_id == self.bot.config["TOURNAMENT_CHANNEL_ID"]:
                await ctx.send("Tournament!")
                author_name = ctx.author.name  # Get the author's name
                category_name = tournament_name or author_name
                guild = ctx.message.guild
                await ctx.send("Setting up tournament...")
                category = await guild.create_category(f"{category_name}'s tournament")

                await guild.create_voice_channel(
                    f"Voice", category=category, reason=None, user_limit=5
                )
                await guild.create_text_channel("Text", category=category, reason=None)
                await ctx.send("Tournament room created!")
        except Exception as e:
            print(f"what? {e}")


# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot) -> None:
    await bot.add_cog(Tournaments(bot))
