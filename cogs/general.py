import platform
import random

import aiohttp
import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context


class General(commands.Cog, name="general"):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.context_menu_user = app_commands.ContextMenu(
            name="Grab ID", callback=self.grab_id
        )
        self.bot.tree.add_command(self.context_menu_user)
        self.context_menu_message = app_commands.ContextMenu(
            name="Remove spoilers", callback=self.remove_spoilers
        )
        self.bot.tree.add_command(self.context_menu_message)
    async def remove_spoilers(
        self, interaction: discord.Interaction, message: discord.Message
    ) -> None:
        spoiler_attachment = None
        for attachment in message.attachments:
            if attachment.is_spoiler():
                spoiler_attachment = attachment
                break
        embed = discord.Embed(
            title="Сообщение без спойлеров",
            description=message.content.replace("||", ""),
            color=0xBEBEFE,
        )
        if spoiler_attachment is not None:
            embed.set_image(url=attachment.url)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    # User context menu command
    async def grab_id(
        self, interaction: discord.Interaction, user: discord.User
    ) -> None:
        embed = discord.Embed(
            description=f"ID {user.mention}: `{user.id}`.",
            color=0xBEBEFE,
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @commands.hybrid_command(
        name="help", description="Список всех загруженных в бота команд."
    )
    async def help(self, context: Context) -> None:
        await context.defer(ephemeral=True)
        prefix = self.bot.config["prefix"]
        embed = discord.Embed(
            title="Help", description="Список доступных команд:", color=0xBEBEFE
        )
        for i in self.bot.cogs:
            if i == "owner" and not (await self.bot.is_owner(context.author)):
                continue
            cog = self.bot.get_cog(i.lower())
            commands = cog.get_commands()
            data = []
            for command in commands:
                description = command.description.partition("\n")[0]
                data.append(f"{prefix}{command.name} - {description}")
            help_text = "\n".join(data)
            embed.add_field(
                name=i.capitalize(), value=f"```{help_text}```", inline=False
            )
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="serverinfo",
        description="Получить различную информацию о сервере.",
    )
    async def serverinfo(self, context: Context) -> None:
        await context.defer(ephemeral=True)
        roles = [role.name for role in context.guild.roles]
        if len(roles) > 50:
            roles = roles[:50]
            roles.append(f">>>> Отображено [50/{len(roles)}] ролей")
        roles = ", ".join(roles)

        embed = discord.Embed(
            title="**Название сервера:**", description=f"{context.guild}", color=0xBEBEFE
        )
        if context.guild.icon is not None:
            embed.set_thumbnail(url=context.guild.icon.url)
        embed.add_field(name="ID Сервера", value=context.guild.id)
        embed.add_field(name="Количество участников", value=context.guild.member_count)
        embed.add_field(
            name="Количество текстовых и войс каналов:", value=f"{len(context.guild.channels)}"
        )
        embed.add_field(name=f"Роли ({len(context.guild.roles)})", value=roles)
        embed.set_footer(text=f"Создана: {context.guild.created_at}")
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="ping",
        description="Проверяет что бот жив.",
    )
    async def ping(self, context: Context) -> None:
        await context.defer(ephemeral=True)
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"Задержка выполнения команд: {round(self.bot.latency * 1000)}мс.",
            color=0xBEBEFE,
        )
        await context.send(embed=embed)
        
    async def bitcoin(self, context: Context) -> None:
        await context.defer(ephemeral=True)
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://api.coindesk.com/v1/bpi/currentprice/BTC.json"
            ) as request:
                if request.status == 200:
                    data = await request.json(
                        content_type="application/javascript"
                    ) 
                    embed = discord.Embed(
                        title="Bitcoin price",
                        description=f"The current price is {data['bpi']['USD']['rate']} :dollar:",
                        color=0xBEBEFE,
                    )
                else:
                    embed = discord.Embed(
                        title="Error!",
                        description="There is something wrong with the API, please try again later",
                        color=0xE02B2B,
                    )
                await context.send(embed=embed)


async def setup(bot) -> None:
    await bot.add_cog(General(bot))
