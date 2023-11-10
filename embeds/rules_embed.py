import discord
import datetime
from discord.ext import commands
from discord.ext.commands import Context


def create_tournament_announcement_embed(
    date, requirements, registration_link, tournament_format, award, banner, description
):
    embed = discord.Embed(
        title="My Amazing Embed",
        description="Embeds are super easy, barely an inconvenience.",
        color=discord.Colour.blurple(),  # Pycord provides a class with default colors you can choose from
    )
    embed.add_field(
        name="A Normal Field",
        value="A really nice field with some information. **The description as well as the fields support markdown!**",
    )
    embed.add_field(name="Inline Field 1", value="Inline Field 1", inline=True)
    embed.add_field(name="Inline Field 2", value="Inline Field 2", inline=True)
    embed.add_field(name="Inline Field 3", value="Inline Field 3", inline=True)

    embed.set_footer(text="Footer! No markdown here.")  # footers can have icons too
    embed.set_author(
        name="Pycord Team",
        icon_url="https://cybersport.metaratings.ru/storage/images/4f/9a/4f9ab43ff49dd6ad63eaf036295f12cb.jpg",
    )
    embed.set_thumbnail(
        url="https://cybersport.metaratings.ru/storage/images/4f/9a/4f9ab43ff49dd6ad63eaf036295f12cb.jpg"
    )
    embed.set_image(
        url="https://cybersport.metaratings.ru/storage/images/4f/9a/4f9ab43ff49dd6ad63eaf036295f12cb.jpg"
    )
    return embed
        # await ctx.send("Hello! Here's a cool embed.", embed=embed) # 