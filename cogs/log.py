from discord.ext import commands
from discord.ext.commands import Context
from discord import Embed
import discord
from datetime import datetime


# Here we name the cog and create a new class for the cog.
class Log(commands.Cog, name="log"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        log_channel = self.bot.get_channel(self.bot.config["LOG_CHANNEL_ID"])
        embed = Embed(title="Member Joined", description=f"{member.mention} joined the server.", color=discord.Color.green())
        embed.set_footer(text=f"User ID: {member.id} | Joined at {member.joined_at}")
        await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        log_channel = self.bot.get_channel(self.bot.config["LOG_CHANNEL_ID"])
        embed = Embed(title="Member Left", description=f"{member.mention} left the server.", color=discord.Color.red())
        embed.set_footer(text=f"User ID: {member.id} | Left at {discord.utils.utcnow()}")
        await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        log_channel = self.bot.get_channel(self.bot.config["LOG_CHANNEL_ID"])
        admin_roles = ["Administrators", "Developers", "move role"]  # List of admin role names

        # Check if the user was self-muted or self-deafened
        if before.self_mute != after.self_mute:
            if after.self_mute:
                message = f"{member.mention} self-muted."
            else:
                message = f"{member.mention} self-unmuted."

            embed = Embed(title="User Action", description=message, color=discord.Color.green())
            embed.timestamp = datetime.now()
            await log_channel.send(embed=embed)

        if before.self_deaf != after.self_deaf:
            if after.self_deaf:
                message = f"{member.mention} self-deafened."
            else:
                message = f"{member.mention} self-undeafened."

            embed = Embed(title="User Action", description=message, color=discord.Color.green())
            embed.timestamp = datetime.now()
            await log_channel.send(embed=embed)

        # Check if the user was moved to a different channel
        if before.channel != after.channel:
            if before.channel:
                # User left the channel
                message = f"{member.mention} left voice channel {before.channel.name}."
            if after.channel:
                # User joined the channel
                message = f"{member.mention} joined voice channel {after.channel.name}."

            embed = Embed(title="User Action", description=message, color=discord.Color.green())
            embed.timestamp = datetime.now()
            log_channel = self.bot.config["LOG_CHANNEL_ID"]
            await log_channel.send(embed=embed)

        if any(role.name in admin_roles for role in member.roles):
            if before.mute != after.mute:
                if after.mute:
                    message = f"{member.mention} was server-muted by an admin."
                else:
                    message = f"{member.mention} was server-unmuted by an admin."

                embed = Embed(title="Admin Action", description=message, color=discord.Color.blue)
                embed.timestamp = datetime.now()
                await log_channel.send(embed=embed)

            if before.deaf != after.deaf:
                if after.deaf:
                    message = f"{member.mention} was server-deafened by an admin."
                else:
                    message = f"{member.mention} was server-undeafened by an admin."

                embed = Embed(title="Admin Action", description=message, color=discord.Color.blue)
                embed.timestamp = datetime.now()
                await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        log_channel = self.bot.get_channel(self.bot.config["LOG_CHANNEL_ID"])
        self.bot.logger.info(f"Message was edited by {after.author.id} at{discord.utils.utcnow()} ")
        embed = discord.Embed(
            title="Message Edited",
            description=f"{after.author.mention} edited a message in {after.channel.mention}",
            color=discord.Color.blue(),
        )
        embed.add_field(name="Before", value=before.content, inline=False)
        embed.add_field(name="After", value=after.content, inline=False)
        embed.set_footer(text=f"User ID: {after.author.id} | Edited at {discord.utils.utcnow()}")
        await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        log_channel = self.bot.get_channel(self.bot.config["LOG_CHANNEL_ID"])
        self.bot.logger.info(f"Message was deleted by {message.author.name} - {message.author.nick} at{discord.utils.utcnow()} ")
        if not message.author.bot:
            embed = Embed(
                title="Message Deleted",
                description=f"{message.author.mention} deleted a message in {message.channel.mention}",
                color=discord.Color.red(),
            )
            embed.add_field(name="Content", value=message.content, inline=False)
            embed.set_footer(text=f"User ID: {message.author.id} | Deleted at {discord.utils.utcnow()}")
            await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        log_channel = self.bot.get_channel(self.bot.config["LOG_CHANNEL_ID"])
        channel_name = channel.name
        self.bot.logger.info(f"Channel deleted: Channel '{channel_name}' was deleted. at{discord.utils.utcnow()} ")
        embed = Embed(title="Channel Deleted", description=f"Channel '{channel_name}' was deleted.", color=discord.Color.red())
        embed.set_footer(text=f"Guild ID: {channel.guild.id} | Deleted at {datetime.now()}")
        await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
        log_channel = self.bot.get_channel(self.bot.config["LOG_CHANNEL_ID"])
        if before.name != after.name:
            embed = Embed(
                title="Channel Renamed", description=f"Channel '{before.name}' was renamed to '{after.name}'.", color=discord.Color.blue()
            )
        else:
            embed = Embed(title="Channel Edited", description=f"Channel '{before.name}' was edited.", color=discord.Color.blue())
        embed.set_footer(text=f"Guild ID: {before.guild.id} | Edited at {datetime.now()}")
        await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        log_channel = self.bot.get_channel(self.bot.config["LOG_CHANNEL_ID"])
        role_name = role.name
        embed = Embed(title="Role Created", description=f"Role '{role_name}' was created.", color=discord.Color.green())
        embed.set_footer(text=f"Guild ID: {role.guild.id} | Created at {datetime.now()}")
        await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        log_channel = self.bot.get_channel(self.bot.config["LOG_CHANNEL_ID"])
        role_name = role.name
        embed = Embed(title="Role Deleted", description=f"Role '{role_name}' was deleted.", color=discord.Color.red())
        embed.set_footer(text=f"Guild ID: {role.guild.id} | Deleted at {datetime.now()}")
        await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_role_update(self, before, after):
        log_channel = self.bot.get_channel(self.bot.config["LOG_CHANNEL_ID"])
        if before.name != after.name:
            embed = Embed(
                title="Role Renamed", description=f"Role '{before.name}' was renamed to '{after.name}'.", color=discord.Color.blue()
            )
        else:
            embed = Embed(title="Role Edited", description=f"Role '{before.name}' was edited.", color=discord.Color.blue())
        embed.set_footer(text=f"Guild ID: {before.guild.id} | Edited at {datetime.now()}")
        await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        log_channel = self.bot.get_channel(self.bot.config["LOG_CHANNEL_ID"])
        channel_name = channel.name
        embed = Embed(title="Channel Created", description=f"Channel '{channel_name}' was created.", color=discord.Color.green())
        embed.set_footer(text=f"Guild ID: {channel.guild.id} | Created at {datetime.now()}")
        await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        log_channel = self.bot.get_channel(self.bot.config["LOG_CHANNEL_ID"])
        channel_name = channel.name
        embed = Embed(title="Channel Deleted", description=f"Channel '{channel_name}' was deleted.", color=discord.Color.red())
        embed.set_footer(text=f"Guild ID: {channel.guild.id} | Deleted at {datetime.now()}")
        await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
        log_channel = self.bot.get_channel(self.bot.config["LOG_CHANNEL_ID"])
        if before.name != after.name:
            embed = Embed(
                title="Channel Renamed", description=f"Channel '{before.name}' was renamed to '{after.name}'.", color=discord.Color.blue()
            )
        else:
            embed = Embed(title="Channel Edited", description=f"Channel '{before.name}' was edited.", color=discord.Color.blue())
        embed.set_footer(text=f"Guild ID: {before.guild.id} | Edited at {datetime.now()}")
        await log_channel.send(embed=embed)


# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot) -> None:
    await bot.add_cog(Log(bot))
