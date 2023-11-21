from discord import Embed

from .url_icons import *
from .embed_utils import *


@success_color()
def get_navigator_roles_wiki_embed() -> Embed:
    embed = Embed()
    embed.add_field(
        "Путник (5+) - даёт возможность стримить в голосовых каналах.", value="", inline=False
    )
    embed.add_field(
        "Рекрут (15+) - позволяет прикреплять картинки и ссылки в любых чатах.",
        value="",
        inline=False,
    )
    embed.add_field(
        "Боец (30+) - доступ к голосовому каналу «Цикламен» и добавляется возможность ставить реакции.",
        value="",
        inline=False,
    )
    embed.add_field(
        "Специалист (50+) - появляется возможность использовать сторонние эмодзи и стикеры.",
        value="",
        inline=False,
    )
    embed.add_field(
        "Мастер (75+) - доступ к приватному гк и чату с модераторами.", value="", inline=False
    )
    embed.add_field(
        "Хранитель (100+) - ваш ник отображается справа, над всеми ролями.", value="", inline=False
    )
    embed.add_field(
        "@・Nitro Booster - открывает возможности с 5 по 50 уровни включительно.",
        value="",
        inline=False,
    )

    return embed


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
