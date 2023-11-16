from discord import Embed, Colour
from discord import Client

ticket_banner = "https://cdn.discordapp.com/attachments/1174664368688996352/1174810471807844544/ticket.png?ex=6568f283&is=65567d83&hm=6d194f2c033efffeea78d650327d33bf04ce9f6dd24e95dbd47847528101c010&"
v_icon_url = "https://cdn.discordapp.com/attachments/1174664368688996352/1174669493683888148/v_icon.png?ex=65686f37&is=6555fa37&hm=f61d317ecfa5e72fb839db3d684f2add8c592c4887825d6f0382974bd232de6b&"
dot_url = "https://cdn.discordapp.com/attachments/1174664368688996352/1174744429861552168/dot.png?ex=6568b501&is=65564001&hm=e91241e4824b9a27827330ede6807148affc84826a4b039a8632fd5e4c3029db&"
star_url = "https://cdn.discordapp.com/attachments/1174664368688996352/1174744769692450916/star.png?ex=6568b552&is=65564052&hm=9cb96a2855f02f5dbd56d733e98a58abf52052329f6ab36fd9bd2e23cccfad81&"


def get_ticket_embed(bot: Client) -> Embed:
    embed = Embed(
        title="Оставьте жалобу на участника",
        color=Colour.from_str(bot.config["INFO_COLOR"]),
    )
    embed.add_field(
        name="",
        value="""```В создавшемся обращении, как можно точнее опишите его суть и по возможности прикрепите фото и/или видео для дальнейшего ознакомления.```""",
        inline=False,
    )
    return embed


def get_report_sent_embed(bot: Client) -> Embed:
    embed = Embed(
        title="Жалоба отправлена!",
        color=Colour.from_str(bot.config["SUCCESS_COLOR"]),
    )
    embed.add_field(
        name="",
        value="""```Наши модераторы в кратчайшие сроки постараются проверить вашу жалому, нарушитель будет наказан!```""",
        inline=False,
    )
    embed.set_footer(
        text="ПРИМЕЧАНИЕ: иногда могут потребоваться скриншоты, видео или другая информация."
    )
    return embed


def get_report_info_embed(bot: Client, author: str, reported_user: str, description: str) -> Embed:
    embed = Embed(
        title="Cоздана новая жалоба на пользователя",
        color=Colour.from_str(bot.config["INFO_COLOR"]),
    )
    embed.add_field(
        name="",
        value=f"""```Автор жалобы: {author}```""",
        inline=False,
    )
    embed.add_field(
        name="",
        value=f"""```Предполагаемый виновник: {reported_user}```""",
        inline=False,
    )
    embed.add_field(
        name="",
        value=f"""```ОПИСАНИЕ: {description}```""",
        inline=False,
    )
    embed.set_footer(
        text="ПРИМЕЧАНИЕ: иногда могут потребоваться скриншоты, видео или другая информация."
    )
    return embed
