import os
from datetime import datetime

import discord
from discord.ext import commands

import asyncio
import random

from PIL import Image, ImageDraw, ImageOps, ImageFont
from io import BytesIO


def square_to_circle(file):
    data = BytesIO(file.fp.read())
    square_img = Image.open(data)
    mask = Image.new("L", square_img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + square_img.size, fill=255)
    circular_img = ImageOps.fit(square_img, mask.size, centering=(0.5, 0.5))
    circular_img.putalpha(mask)
    return circular_img


def add_text(image, username):
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("src/V.ttf", 80)
    draw.text((730, 170), username, (255, 255, 255), font=font)
    # Draw a rounded rectangle
    draw.rounded_rectangle((714, 572, 1809, 615), fill="orange", radius=100)
    return image


class Avatar(commands.Cog, name="avatar"):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.guild = self.bot.get_guild(self.bot.config["GUILD_ID"])

    @commands.hybrid_command(
        name="avatar",
        with_app_command=True,
        description="Отображает твой профиль на сервере",
    )
    @commands.has_role("Member")
    async def avatar(self, ctx, user_id=None):
        if user_id is None:
            user = ctx.author
        else:
            user = self.bot.get_user(int(user_id))
        # loading background
        background = Image.open("src/img/background.png")
        background = add_text(background, user.name)

        avatar = await user.avatar.to_file(filename="avatar.png")
        circular_avatar = square_to_circle(avatar).resize((586, 586), Image.Resampling.LANCZOS)

        background.paste(circular_avatar, (56, 62), circular_avatar)

        # Save the final image and send it in the chat
        background.save("src/img/user_profile.png")
        await ctx.send(file=discord.File("src/img/user_profile.png"))


async def setup(bot) -> None:
    await bot.add_cog(Avatar(bot))
