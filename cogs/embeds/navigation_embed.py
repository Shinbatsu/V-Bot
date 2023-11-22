from discord import Embed

from .url_icons import *
from .embed_utils import *


@with_date()
@success_color()
def get_navigation_room_embed() -> Embed:
    embed = Embed()
    embed.set_author(
        name="Перейдите в раздел, нажав на него в меню выбора.",
        icon_url=star_url,
    )
    embed.add_field(
        name=f"{dot} **Роли** — информация о ролях сервера.",
        value="",
        inline=False,
    )
    embed.add_field(
        name=f"{dot} **Профиль** — узнать о своем профиле на сервере.",
        value="",
        inline=False,
    )
    embed.add_field(
        name=f"{dot} **Настройки** — настрой свою личную комнату.",
        value="",
        inline=False,
    )
    return embed
