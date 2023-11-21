import os
from datetime import datetime

import discord
from discord.ext import commands

import asyncio
import random

from PIL import Image, ImageDraw, ImageOps, ImageFont
from io import BytesIO
from discord import app_commands
from discord.ext.commands import Context


def square_to_circle(file):
    data = BytesIO(file.fp.read())
    square_img = Image.open(data)
    mask = Image.new("L", square_img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + square_img.size, fill=255)
    circular_img = ImageOps.fit(square_img, mask.size, centering=(0.5, 0.5))
    circular_img.putalpha(mask)
    return circular_img


class Avatar(commands.Cog, name="avatar"):
    def __init__(self, bot) -> None:
        self.bot = bot

    def add_name(self, image, user):
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype("src/V.ttf", 80)
        draw.text((730, 170), user.name, (255, 255, 255), font=font)
        return image

    def format_activity(self, activity):
        hours = activity // 3600
        minutes = activity // 60
        activity = f"VOICE: {str(hours) + ' H, ' if hours>0 else ''}{str(minutes) + ' M.'}"
        return activity

    def format_all_level(self, activity):
        activity = f"LEVEL: {activity//500+1}"
        return activity

    def add_all_level(self, image, activity):
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype("src/V.ttf", 60)

        draw.text((735, 426), self.format_all_level(activity), (255, 255, 255), font=font)
        return image

    def add_activity(self, image, activity):
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype("src/V.ttf", 60)

        draw.text((735, 326), self.format_activity(activity), (255, 255, 255), font=font)
        return image

    def format_level(self, acitivity):
        return f"{str(acitivity%500)}/500"

    def add_level(self, image, activity):
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype("src/V.ttf", 60)
        draw.text((1570, 510), self.format_level(activity), (255, 255, 255), font=font)
        return image

    def add_progress(self, image, activity):
        bar_size = 1095
        activity = 401
        size = int((bar_size / 100) * (activity / 500 * 100))
        draw = ImageDraw.Draw(image)
        draw.rounded_rectangle((714, 578, 714 + size, 615), fill="white", radius=100)
        return image

    def add_progress_mask(self, image, activity):
        bar_size = 1095
        activity = 401
        size = int((bar_size / 100) * (activity / 500 * 100))
        draw = ImageDraw.Draw(image)
        draw.rounded_rectangle((714, 578, 714 + size, 615), fill=(120, 120, 120), radius=100)
        return image

    @commands.hybrid_command(name="avatar", description="Отображает твой профиль на сервере")
    async def _avatar(self, context: Context, *, user: discord.Member = None) -> None:
        self.bot.logger.info(type(context))
        await context.defer(ephemeral=True)
        await context.send("Рисую аватарку...", ephemeral=True)
        if user is None:
            user = context.author
        background = Image.open("src/img/background.png")
        activity = int(await self.bot.database.get_user_activity(user.id))
        background = self.add_progress(background, activity)
        mask = Image.open("src/img/background_m.png")
        mask = self.add_progress_mask(mask, activity)
        mask = mask.convert("L")
        toner = Image.new(
            "RGBA",
            background.size,
            tuple([random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]),
        )
        background = Image.composite(background, toner, mask)
        avatar = await user.avatar.to_file(filename="avatar.png")
        circular_avatar = square_to_circle(avatar).resize((586, 586), Image.Resampling.LANCZOS)
        background = self.add_level(background, activity)
        background = self.add_all_level(background, activity)
        background = self.add_name(background, user)
        background = self.add_activity(background, activity)
        background.paste(circular_avatar, (56, 62), circular_avatar)
        # background = self.add_progress(background, activity)
        # Save the final image and send it in the chat
        background.save("src/img/user_profile.png")
        await context.send(file=discord.File("src/img/user_profile.png"))


async def setup(bot) -> None:
    await bot.add_cog(Avatar(bot))
