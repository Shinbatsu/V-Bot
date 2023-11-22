import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
from discord import app_commands

class Owner(commands.Cog, name="owner"):
    def __init__(self, bot) -> None:
        self.bot = bot
    @commands.command(
        name="sync",
        description="Synchonizes the slash commands.",
    )
    @app_commands.describe(scope="The scope of the sync. Can be `global` or `guild`")
    @commands.is_owner()
    async def sync(self, context: Context, scope: str = "global") -> None:
        if scope == "global":
            await context.bot.tree.sync()
            embed = discord.Embed(
                description="Slash commands have been globally synchronized.",
                color=0xBEBEFE,
            )
            await context.send(embed=embed,ephemeral=True)
            return
        elif scope == "guild":
            context.bot.tree.copy_global_to(guild=context.guild)
            await context.bot.tree.sync(guild=context.guild)
            embed = discord.Embed(
                description="Слеш команды на этом сервере были синхронизированы.",
                color=0xBEBEFE,
            )
            await context.send(embed=embed)
            return
        embed = discord.Embed(description="Область должна иметь значения `global` или `guild`.", color=0xE02B2B)
        await context.send(embed=embed)

    @commands.command(
        name="unsync",
        description="Отключить слеш команды.",
    )
    @app_commands.describe(
        scope="Пространство выполнения. Может быть `global`, `current_guild` или `guild`"
    )
    @commands.is_owner()
    async def unsync(self, context: Context, scope: str) -> None:
        if scope == "global":
            context.bot.tree.clear_commands(guild=None)
            await context.bot.tree.sync()
            embed = discord.Embed(
                description="Слеш команды были отключены глобально.",
                color=0xBEBEFE,
            )
            await context.send(embed=embed)
            return
        elif scope == "guild":
            context.bot.tree.clear_commands(guild=context.guild)
            await context.bot.tree.sync(guild=context.guild)
            embed = discord.Embed(
                description="Слеш команды на этом сервере были отключены.",
                color=0xBEBEFE,
            )
            await context.send(embed=embed)
            return
        embed = discord.Embed(description="The scope must be `global` or `guild`.", color=0xE02B2B)
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="load",
        description="Загружает модуль",
    )
    @app_commands.describe(cog="Название модуля для загрузки")
    @commands.is_owner()
    async def load(self, context: Context, cog: str) -> None:
        await context.defer(ephemeral=True)
        try:
            await self.bot.load_extension(f"cogs.{cog}")
        except Exception:
            embed = discord.Embed(description=f"Не смог загрузить `{cog}` модуль.", color=0xE02B2B)
            await context.send(embed=embed)
            return
        embed = discord.Embed(description=f"Модуль `{cog}` успешно загружен.", color=0xBEBEFE)
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="unload",
        description="Отключить модуль.",
    )
    @app_commands.describe(cog="Отключаемый модуль")
    @commands.is_owner()
    async def unload(self, context: Context, cog: str) -> None:
        await context.defer(ephemeral=True)
        try:
            await self.bot.unload_extension(f"cogs.{cog}")
        except Exception:
            embed = discord.Embed(description=f"Не смог отключить `{cog}` модуль.", color=0xE02B2B)
            await context.send(embed=embed)
            return
        embed = discord.Embed(description=f"Модуль `{cog}` успешно отключен.", color=0xBEBEFE)
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="reload",
        description="Перезагрузить модуль.",
    )
    @app_commands.describe(cog="Перезагружаемый модуль")
    @commands.is_owner()
    async def reload(self, context: Context, cog: str) -> None:
        await context.defer(ephemeral=True)
        try:
            await self.bot.reload_extension(f"cogs.{cog}")
        except Exception:
            embed = discord.Embed(description=f"Не смог перезагрузить `{cog}` модуль.", color=0xE02B2B)
            await context.send(embed=embed)
            return
        embed = discord.Embed(description=f"Модуль `{cog}` успешно перезагружен.", color=0xBEBEFE)
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="shutdown",
        description="Выключить бота.",
    )
    @commands.is_owner()
    async def shutdown(self, context: Context) -> None:
        await context.defer(ephemeral=True)
        embed = discord.Embed(description="Выключение... Пока! :wave:", color=0xBEBEFE)
        await context.send(embed=embed)
        await self.bot.close()

    @commands.hybrid_command(
        name="say",
        description="Бот скажет, то что захочешь",
    )
    @app_commands.describe(message="Сообщение, которое бот должен повторить")
    @commands.is_owner()
    async def say(self, context: Context, *, message: str) -> None:
        await context.defer(ephemeral=True)
        await context.send(message)

    @commands.hybrid_command(
        name="embed",
        description="Бот скажет, то что захочешь использую embed",
    )
    @app_commands.describe(message="Сообщение, которое бот должен повторить")
    @commands.is_owner()
    async def embed(self, context: Context, *, message: str) -> None:
        await context.defer(ephemeral=True)
        embed = discord.Embed(description=message, color=0xBEBEFE)
        await context.send(embed=embed)


async def setup(bot) -> None:
    await bot.add_cog(Owner(bot))
