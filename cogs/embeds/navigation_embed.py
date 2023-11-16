from discord import Embed, Colour
from discord import Client

navigation_banner = "https://cdn.discordapp.com/attachments/1174664368688996352/1174737992783503503/navigation.png?ex=6568af03&is=65563a03&hm=ed11702f0ad211eccf9ec2e3d6941d57858eeeef26326c948f7d64e891dff55d&"


def get_navigator_banner_embed(bot: Client) -> Embed:
    embed = Embed(
        color=Colour.from_str(bot.config["SUCCESS_COLOR"]),
    )
    # emoji = get(ctx.message.server.emojis, name="emoji1")
    # embed = Embed(title=f"Here is the **title**! {emoji}", color=0x24045b, description=f"Here is the emoji again! {emoji}")
    return embed


def get_navigator_roles_wiki_embed(bot: Client) -> Embed:
    embed = Embed(
        color=Colour.from_str(bot.config["SUCCESS_COLOR"]),
    )
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


def get_navigation_room_embed(bot: Client) -> Embed:
    v_icon_url = "https://cdn.discordapp.com/attachments/1174664368688996352/1174669493683888148/v_icon.png?ex=65686f37&is=6555fa37&hm=f61d317ecfa5e72fb839db3d684f2add8c592c4887825d6f0382974bd232de6b&"
    embed = Embed(
        color=Colour.from_str(bot.config["SUCCESS_COLOR"]),
    )
    embed.set_author(
        name="Перейдите в раздел, нажав на него в меню выбора.",
        icon_url=v_icon_url,
    )
    embed.add_field(
        name=f"<:minidot:1174667819917520966> Роли — информация о ролях сервера.",
        value="",
        inline=False,
    )
    embed.add_field(
        name=f"<:minidot:1174667819917520966> Ранг — узнать о ранге на сервере.",
        value="",
        inline=False,
    )
    embed.set_footer(text="", icon_url=v_icon_url)
    return embed


# :mini_gray:Роли — информация о ролях сервера.
# :mini_gray:Соц. сети — социальные сети VALORANT'a.
# :mini_gray:Турниры — связь насчёт проведения турниров.
# :mini_gray:Подписки — друзья нашего сервера.
# :mini_gray:Партнёры — команда, работающая над сервером.
