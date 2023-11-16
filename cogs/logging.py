from discord.ext import commands
from discord.ext.commands import Context
from discord import Embed, Colour
import discord
from datetime import datetime


# Here we name the cog and create a new class for the cog.
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
            title="Member Joined",
            description=f"{member.mention} joined the server.",
            color=discord.Color.green(),
        )
        embed.set_footer(text=f"User ID: {member.id} | Joined at {member.joined_at}")
        await self.log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        embed = Embed(
            title="Member Left",
            description=f"{member.mention} left the server.",
            color=discord.Color.red(),
        )
        embed.set_footer(text=f"User ID: {member.id} | Left at {discord.utils.utcnow()}")
        await self.log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        self.bot.logger.info(f"Состояние голосового канала изменено {after.author.id} в {discord.utils.utcnow()} ")
        # Check if the user was self-muted or self-deafened
        if before.self_mute != after.self_mute:
            if after.self_mute:
                message = f"{member.mention} замутился."
            else:
                message = f"{member.mention} размутился."

            embed = Embed(title="Действие пользователя:", description=message, color=discord.Color.green())
            embed.timestamp = datetime.now()
            await self.log_channel.send(embed=embed)

        if before.self_deaf != after.self_deaf:
            if after.self_deaf:
                message = f"{member.mention} отключил звук."
            else:
                message = f"{member.mention} включил звук."

            embed = Embed(title="User Action", description=message, color=discord.Color.green())
            embed.timestamp = datetime.now()
            await self.log_channel.send(embed=embed)

        # Check if the user was moved to a different channel
        if before.channel != after.channel:
            if before.channel:
                # User left the channel
                message = f"{member.mention} покинул голосовой канал {before.channel.name}."
            if after.channel:
                # User joined the channel
                message = f"{member.mention} присоединился к голосовому каналу {after.channel.name}."

            embed = Embed(title="Действие пользователя", description=message, color=Colour.from_str(self.bot.config["INFO_COLOR"]),)
            embed.timestamp = datetime.now()
            await self.log_channel.send(embed=embed)

            if before.mute != after.mute:
                if after.mute:
                    message = f"{member.mention} was server-muted by an admin."
                else:
                    message = f"{member.mention} was server-unmuted by an admin."

                embed = Embed(title="Действие Администратора", description=message, color=Colour.from_str(self.bot.config["INFO_COLOR"]),)
                embed.timestamp = datetime.now()
                await self.log_channel.send(embed=embed)

            if before.deaf != after.deaf:
                if after.deaf:
                    message = f"{member.mention} was server-deafened by an admin."
                else:
                    message = f"{member.mention} was server-undeafened by an admin."

                embed = Embed(title="Admin Action", description=message, color=Colour.from_str(self.bot.config["INFO_COLOR"]),)
                embed.timestamp = datetime.now()
                await self.log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        self.bot.logger.info(f"Message was edited by {after.author.id} at{discord.utils.utcnow()} ")
        embed = discord.Embed(
            title="Сообщение редактировано",
            description=f"{after.author.mention} edited a message in {after.channel.mention}",
            color=Colour.from_str(self.bot.config["INFO_COLOR"]),
        )
        embed.add_field(name="До: ", value=before.content, inline=False)
        embed.add_field(name="После: ", value=after.content, inline=False)
        embed.set_footer(text=f"User ID: {after.author.id} | Изменено: {discord.utils.utcnow()}")
        await self.log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        self.bot.logger.info(
            f"Message was deleted by {message.author.name} - {message.author.nick} at{discord.utils.utcnow()} "
        )
        if not message.author.bot:
            embed = Embed(
                title="Cообщение удалено",
                description=f"Сообщение в канале {message.channel.mention} удалено {message.author.mention}.",
                color=discord.Color.red(),
            )
            embed.add_field(name="Содержание", value=message.content, inline=False)
            embed.set_footer(
                text=f"User ID: {message.author.id} | Удалено: {discord.utils.utcnow()}"
            )
            await self.log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        channel_name = channel.name
        entry = await channel.guild.audit_logs(action=discord.AuditLogAction.channel_delete, limit=1).get()
        self.bot.logger.info(
            f"Channel deleted: Channel '{channel_name}' was deleted. at{discord.utils.utcnow()} "
        )
        embed = Embed(
            title="Комната удалена",
            description=f"Комната '{channel_name}' была удалена {entry.user.name}.",
            color=discord.Color.red(),
        )
        embed.set_footer(text=f"Guild ID: {channel.guild.id} | Deleted at {datetime.now()}")
        await self.log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
        if before.name != after.name:
            embed = Embed(
                title="Комната переименована",
                description=f"Комната '{before.name}'была переименована в '{after.name}'.",
                color=discord.Color.blue(),
            )
        else:
            embed = Embed(
                title="Комната была изменена",
                description=f"Комната '{before.name}' была изменена.",
                color=discord.Color.blue(),
            )
        embed.set_footer(text=f"Guild ID: {before.guild.id} | Edited at {datetime.now()}")
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
                description=f"Role '{before.name}' was renamed to '{after.name}'.",
                color=Colour.from_str(self.bot.config["INFO_COLOR"]),
            )
        else:
            embed = Embed(
                title="Параметры роли изменены",
                description=f"Роль '{before.name}' была изменена.",
                color=Colour.from_str(self.bot.config["INFO_COLOR"]),
            )
        embed.set_footer(text=f"Сервер ID: {before.guild.id} | Изменено: {datetime.now()}")
        await self.log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        channel_name = channel.name
        embed = Embed(
            title="Channel Created",
            description=f"Channel '{channel_name}' was created.",
            color=discord.Color.green(),
        )
        embed.set_footer(text=f"Guild ID: {channel.guild.id} | Создано: {datetime.now()}")
        await self.log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        channel_name = channel.name
        embed = Embed(
            title="Channel Deleted",
            description=f"Channel '{channel_name}' was deleted.",
            color=discord.Color.red(),
        )
        embed.set_footer(text=f"Guild ID: {channel.guild.id} | Deleted at {datetime.now()}")
        await self.log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
        if before.name != after.name:
            embed = Embed(
                title="Channel Renamed",
                description=f"Channel '{before.name}' was renamed to '{after.name}'.",
                color=discord.Color.blue(),
            )
        else:
            embed = Embed(
                title="Channel Edited",
                description=f"Channel '{before.name}' was edited.",
                color=discord.Color.blue(),
            )
        embed.set_footer(text=f"Guild ID: {before.guild.id} | Edited at {datetime.now()}")
        await self.log_channel.send(embed=embed)


# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot) -> None:
    await bot.add_cog(Log(bot))
