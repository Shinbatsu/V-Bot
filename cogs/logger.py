from discord.ext import commands
from discord.ext.commands import Context
from discord import Embed, Colour
import discord
from datetime import datetime
from discord import app_commands

class Log(commands.Cog, name="log"):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.log_channel = None

    @commands.Cog.listener()
    async def on_ready(self):
        self.log_channel = self.bot.get_channel(self.bot.config["LOG_CHANNEL_ID"])

    @commands.Cog.listener()
    async def on_member_join(self, member):
        embed = Embed(
            title="Новый участник",
            description=f"{member.mention} присоединился к серверу.",
            color=Colour.from_str(self.bot.config["SUCCESS_COLOR"]),
        )
        embed.set_footer(text=f"User ID: {member.id} | Вошел: {member.joined_at}")
        await self.log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        embed = Embed(
            title="Участник покинул сервер",
            description=f"{member.mention} покинул этот сервер.",
            color=Colour.from_str(self.bot.config["ERROR_COLOR"]),
        )
        embed.set_footer(text=f"User ID: {member.id} | Вышел: {discord.utils.utcnow()}")
        await self.log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if before.self_mute != after.self_mute:
            if after.self_mute:
                message = f"{member.mention} замутился."
            else:
                message = f"{member.mention} размутился."

            embed = Embed(
                title="Действие пользователя:",
                description=message,
                color=Colour.from_str(self.bot.config["INFO_COLOR"]),
            )
            embed.timestamp = datetime.now()
            await self.log_channel.send(embed=embed)

        if before.self_deaf != after.self_deaf:
            if after.self_deaf:
                message = f"{member.mention} отключил звук."
            else:
                message = f"{member.mention} включил звук."

            embed = Embed(
                title="Действие пользователя",
                description=message,
                color=Colour.from_str(self.bot.config["INFO_COLOR"]),
            )
            embed.set_footer(text=f"User ID: {member.id} | Изменено: {discord.utils.utcnow()}")
            await self.log_channel.send(embed=embed)

        if before.channel != after.channel:
            if before.channel:
                message = f"{member.mention} покинул голосовой канал {before.channel.name}."
            if after.channel:
                message = (
                    f"{member.mention} присоединился к голосовому каналу {after.channel.jump_url}."
                )
            embed = Embed(
                title="Действие пользователя",
                description=message,
                color=Colour.from_str(self.bot.config["INFO_COLOR"]),
            )
            embed.set_footer(text=f"User ID: {member.id} | Изменено: {discord.utils.utcnow()}")
            await self.log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if after.channel.id == self.bot.config["REPORT_CHANNEL_ID"]:
            return
        embed = discord.Embed(
            title="Сообщение редактировано",
            description=f"{after.author.mention} изменил сообщение в {after.channel.jump_url}",
            color=Colour.from_str(self.bot.config["INFO_COLOR"]),
        )
        embed.add_field(name="До: ", value=before.content, inline=False)
        embed.add_field(name="После: ", value=after.content, inline=False)
        embed.set_footer(text=f"User ID: {after.author.id} | Изменено: {discord.utils.utcnow()}")
        await self.log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if not message.author.bot:
            embed = Embed(
                title="Cообщение удалено",
                description=f"Сообщение в канале {message.channel.mention} удалено {message.author.mention}.",
                color=Colour.from_str(self.bot.config["ERROR_COLOR"]),
            )
            embed.add_field(name="Содержание", value=message.content, inline=False)
            embed.set_footer(
                text=f"User ID: {message.author.id} | Удалено: {discord.utils.utcnow()}"
            )
            await self.log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        channel_name = channel.name
        entry = await channel.guild.audit_logs(
            action=discord.AuditLogAction.channel_delete, limit=1
        ).get()
        embed = Embed(
            title="Комната удалена",
            description=f"Комната '{channel_name}' была удалена {entry.user.name}.",
            color=discord.Color.red(),
        )
        embed.set_footer(text=f"Guild ID: {channel.guild.id} | Удалено: {datetime.now()}")
        await self.log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
        if before.name != after.name:
            embed = Embed(
                title="Комната переименована",
                description=f"Комната '{before.name}' | Изменено: '{after.name}'.",
                color=discord.Color.blue(),
            )
            embed.set_footer(text=f"Сервер ID: {before.guild.id} | Изменено: {datetime.now()}")
            await self.log_channel.send(embed=embed)
        else:
            embed = Embed(
                title="Комната была изменена",
                description=f"Комната '{before.name}' была изменена.",
                color=discord.Color.blue(),
            )
        embed.set_footer(text=f"Guild ID: {before.guild.id} | Изменено: {datetime.now()}")
        await self.log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        role_name = role.name
        embed = Embed(
            title="Роль создана",
            description=f"Роль '{role_name}' была создана.",
            color=Colour.from_str(self.bot.config["INFO_COLOR"]),
        )
        embed.set_footer(text=f"Сервер ID: {role.guild.id} | Создана: {datetime.now()}")
        await self.log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        role_name = role.name
        embed = Embed(
            title="Роль удалена",
            description=f"Роль '{role_name}' была удалена.",
            color=Colour.from_str(self.bot.config["ERROR_COLOR"]),
        )
        embed.set_footer(text=f"Сервер ID: {role.guild.id} | Удалена {datetime.now()}")
        await self.log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_role_update(self, before, after):
        if before.name != after.name:
            embed = Embed(
                title="Роль переименована",
                description=f"Роль '{before.name}' была переименована в '{after.name}'.",
                color=Colour.from_str(self.bot.config["INFO_COLOR"]),
            )
            embed.set_footer(text=f"Сервер ID: {before.guild.id} | Изменено: {datetime.now()}")
            await self.log_channel.send(embed=embed)
        elif before.permissions != after.permissions:
            for perm, value in before.permissions:
                av = getattr(after.permissions, perm)
                embed = Embed(
                    title="Права роли изменены",
                    description=f"Права роли были {'добавлены' if av else 'убраны, {value}'}.",
                    color=Colour.from_str(self.bot.config["INFO_COLOR"]),
                )
                embed.set_footer(text=f"Сервер ID: {before.guild.id} | Изменено: {datetime.now()}")
                await self.log_channel.send(embed=embed)
        elif before.position != after.position:
            return
        elif before.color != after.color:
            embed = Embed(
                title="Цвет роли был изменен",
                description=f"Цвет роли '{before.name}' был изменен с { before.color} на {after.color}.",
                color=Colour.from_str(self.bot.config["INFO_COLOR"]),
            )
            embed.set_footer(text=f"Сервер ID: {before.guild.id} | Изменено: {datetime.now()}")
            await self.log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        channel_name = channel.name
        embed = Embed(
            title="Канал создан",
            description=f"Channel '{channel_name}' was created.",
            color=discord.Color.green(),
        )
        embed.set_footer(text=f"Guild ID: {channel.guild.id} | Создано: {datetime.now()}")
        await self.log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        channel_name = channel.name
        embed = Embed(
            title="Канал удален",
            description=f"Канал '{channel_name}' был удален.",
            color=discord.Color.red(),
        )
        embed.set_footer(text=f"Guild ID: {channel.guild.id} | Deleted at {datetime.now()}")
        await self.log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
        if before.name != after.name:
            embed = Embed(
                title="Канал переименован",
                description=f"Канал '{before.name}' был переименован в '{after.name}'.",
                color=discord.Color.blue(),
            )
        else:
            embed = Embed(
                title="Канал изменен",
                description=f"Канал '{before.name}' был изменен.",
                color=discord.Color.blue(),
            )
        embed.set_footer(text=f"Guild ID: {before.guild.id} | Edited at {datetime.now()}")
        await self.log_channel.send(embed=embed)


async def setup(bot) -> None:
    await bot.add_cog(Log(bot))
