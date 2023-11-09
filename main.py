# import os
# import asyncio

# import discord
# from discord.ext import commands
# from config import settings

# bot = commands.Bot(
#     command_prefix=settings["prefix"],
#     intents=discord.Intents.all(),
#     case_insensitive=True,
# )


# class MyCog(commands.Cog):
#     def __init__(self, bot):
#         self.bot = bot

#     @commands.command()
#     async def baz(self, ctx):
#         await ctx.send("something")




# async def load():
#     for filename in os.listdir("./cogs"):
#         if filename.endswith(".py"):
#             await bot.load_extension(f"cogs.{filename[:-3]}")


# async def main():
#     await load()
#     # activity = discord.Game(name="with the API")
#     # await bot.change_presence(status=discord.Status.idle, activity=activity)
#     await bot.start(settings["token"])


# if __name__ == "__main__":
#     asyncio.run(main())
