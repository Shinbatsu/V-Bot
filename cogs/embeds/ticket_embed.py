from discord import Embed, Colour
from discord import Client
from datetime import datetime
from .url_icons import *
from .embed_utils import *

@error_color()
def get_slow_down_embed(bot: Client, cooldown: float) -> Embed:
    embed = Embed(
        title="Подождите!",
    )
    embed.add_field(
        name=f"Нельзя использовать так часто! Попробуйте снова через {cooldown} сек.", value=""
    )
    return embed

@info_color()
def get_ticket_embed(bot: Client) -> Embed:
    embed = Embed()
    embed.set_author(icon_url=star_url, name=" Оставьте жалобу на участника")
    embed.add_field(
        name="",
        value=f"""```В создавшемся обращении как можно точнее опишите \nего причину, ссылки на фото и/или видео для \nдальнейшего ознакомления.```""",
        inline=False,
    )
    embed.add_field(
        name="",
        value=f"""```В случае жалобы на группу участников, укажите \nвсех участников в вашем обращении.```""",
        inline=False,
    )
    embed.add_field(
        name="",
        value=f"""{div}""",
        inline=False,
    )
    embed.add_field(
        name="",
        value=f"""```Примечание: Жалобы можно отправлять не чаще чем \n1 раз за 30 минут.```""",
        inline=False,
    )
    return embed


@success_color()
def get_report_sent_embed(bot: Client) -> Embed:
    embed = Embed()
    embed.set_author(icon_url=dot_url, name=" Оставьте жалобу на участника")
    embed.add_field(
        name="",
        value="""```Наши модераторы в кратчайшие сроки постараются проверить вашу жалому, нарушитель будет наказан!```""",
        inline=False,
    )
    embed.set_footer(
        text="Иногда для проверки жалобы могут потребоваться скриншоты, видео или другая информация."
    )
    return embed


def get_self_report_embed(bot: Client) -> Embed:
    embed = Embed(
        title="Попытка саморепорта!",
        color=Colour.from_str(bot.config["ERROR_COLOR"]),
    )
    embed.add_field(
        name="",
        value="""```Похоже что вы указали собственный ID, в качетве того, \nкто по вашему мнению является виноватым! Ваш запрос был отклонен!```""",
        inline=False,
    )
    return embed


def get_report_info_embed(bot: Client, author: str, reported_user: str, description: str) -> Embed:
    embed = Embed(
        title="Cоздана новая жалоба на пользователя",
        color=Colour.from_str(bot.config["INFO_COLOR"]),
    )
    embed.add_field(
        name=f"""{dot}Автор: {author}""",
        value="",
        inline=False,
    )
    embed.add_field(
        name=f"""```{dot}Виновник: {reported_user}```""",
        value="" ,
        inline=False,
    )
    embed.add_field(
        name=f"""{dot}Описание: {description}""",
        value="",
        inline=False,
    )
    embed.add_field(
        name="",
        value=f"""{div}""",
        inline=False,
    )
    embed.set_footer(
        text="ПРИМЕЧАНИЕ: Иногда могут потребоваться скриншоты, видео или другая информация."
    )
    return embed


### ЖАЛОБА ЗАКРЫТА
def get_report_was_resolved_embed(bot: Client, jump_url, moderator_name) -> Embed:
    embed = Embed(
        title="Жалоба закрыта",
        color=Colour.from_str(bot.config["INFO_COLOR"]),
    )
    embed.add_field(
        name="",
        value=f"""[Заявка]({jump_url}) ```была разрешена модератором {moderator_name}.```""",
        inline=False,
    )
    embed.set_footer(text=f"Дата: {datetime.now()}")
    return embed


### ПРЕДУПРЕЖДЕНИЕ
def get_user_warn_embed(bot: Client, description: str) -> Embed:
    embed = Embed(
        title="Замечание",
        color=Colour.from_str(bot.config["ERROR_COLOR"]),
    )
    embed.add_field(name="", value=f"```ПРИЧИНА: {description.capitalize()}```")
    embed.set_footer(text=f"Дата: {datetime.now()}")
    return embed


def get_user_warn_sent_embed(bot: Client) -> Embed:
    embed = Embed(
        title="Замечание",
        color=Colour.from_str(bot.config["SUCCESS_COLOR"]),
    )
    embed.add_field(
        name="",
        value="```Замечание пользователю было успешно отправлено!```",
        inline=False,
    )
    embed.set_footer(text=f"Дата: {datetime.now()}")
    return embed


### КИК
def get_user_kick_embed(bot: Client, description: str) -> Embed:
    embed = Embed(
        title="Кик",
        color=Colour.from_str(bot.config["ERROR_COLOR"]),
    )
    embed.add_field(
        name="",
        value=f"```Модерация вас кикнула с сервера!```",
        inline=False,
    )
    embed.add_field(
        name="",
        value=f"```ПРИЧИНА: {description}```",
        inline=False,
    )
    embed.set_footer(text=f"Дата: {datetime.now()}")
    return embed


def get_user_kick_sent_embed(bot: Client) -> Embed:
    embed = Embed(
        title="Кик",
        color=Colour.from_str(bot.config["SUCCESS_COLOR"]),
    )
    embed.add_field(
        name="",
        value="```Пользователь был успешно кикнут!```",
        inline=False,
    )
    embed.set_footer(text=f"Дата: {datetime.now()}")

    return embed


### ВРЕМЕННЫЙ МУТ
def get_user_temp_mute_embed(bot: Client, description: str, time: int) -> Embed:
    embed = Embed(
        title="Временный мут",
        color=Colour.from_str(bot.config["ERROR_COLOR"]),
    )
    embed.add_field(
        name="",
        value=f"```Модерация запретила вам использовать голосовые сообщение в течении следующих: {time} сек.```",
        inline=False,
    )
    embed.add_field(
        name="",
        value=f"```ПРИЧИНА: {description}```",
        inline=False,
    )
    embed.set_footer(text=f"Дата: {datetime.now()}")
    return embed


def get_user_temp_mute_sent_embed(bot: Client) -> Embed:
    embed = Embed(
        title="Временный мут",
        color=Colour.from_str(bot.config["SUCCESS_COLOR"]),
    )
    embed.add_field(
        name="",
        value="```Пользователю было успешно запрещено говорить!```",
        inline=False,
    )
    embed.set_footer(text=f"Дата: {datetime.now()}")
    return embed


def get_user_unmute_embed(bot: Client) -> Embed:
    embed = Embed(
        title="Временный мут",
        color=Colour.from_str(bot.config["SUCCESS_COLOR"]),
    )
    embed.add_field(
        name="",
        value=f"```Теперь вам снова разрешено использовать голосовые сообщения!```",
        inline=False,
    )
    embed.set_footer(text=f"Дата: {datetime.now()}")
    return embed
    ### ВРЕМЕННЫЙ ЗАПРЕТ ПЕЧАТИ


def get_user_temp_stop_typing_embed(bot: Client, description: str, time: int) -> Embed:
    embed = Embed(
        title="Временный мут",
        color=Colour.from_str(bot.config["ERROR_COLOR"]),
    )
    embed.add_field(
        name="",
        value=f"```Модерация запретила вам использовать текстовый чат в течении следующих: {time} сек.```",
        inline=False,
    )
    embed.add_field(
        name="",
        value=f"```ПРИЧИНА: {description}```",
        inline=False,
    )
    embed.set_footer(text=f"Дата: {datetime.now()}")
    return embed


def get_user_temp_stop_typing_sent_embed(bot: Client) -> Embed:
    embed = Embed(
        title="Временный мут",
        color=Colour.from_str(bot.config["SUCCESS_COLOR"]),
    )
    embed.add_field(
        name="",
        value="```Пользователю было успешно запрещено использовать текстовый чат!```",
        inline=False,
    )
    embed.set_footer(text=f"Дата: {datetime.now()}")
    return embed


def get_user_temp_unstop_typing_embed(bot: Client) -> Embed:
    embed = Embed(
        title="Временный мут",
        color=Colour.from_str(bot.config["SUCCESS_COLOR"]),
    )
    embed.add_field(
        name="",
        value=f"```Теперь вам снова разрешено использовать текстовый чат!```",
        inline=False,
    )
    embed.set_footer(text=f"Дата: {datetime.now()}")
    return embed


### ВРЕМЕННЫЙ БАН
def get_user_temp_ban_embed(bot: Client, description: str, time: int) -> Embed:
    embed = Embed(
        title="Временная блокировка",
        color=Colour.from_str(bot.config["ERROR_COLOR"]),
    )
    embed.add_field(
        name="",
        value=f"```Модерация запретила вам посещать сервер в течении следующих: {time} сек.```",
        inline=False,
    )
    embed.add_field(
        name="",
        value=f"```ПРИЧИНА: {description}```",
        inline=False,
    )
    embed.set_footer(text=f"Дата: {datetime.now()}")
    return embed


def get_user_temp_ban_sent_embed(bot: Client) -> Embed:
    embed = Embed(
        title="Временная блокировка",
        color=Colour.from_str(bot.config["SUCCESS_COLOR"]),
    )
    embed.add_field(
        name="",
        value="```Пользователь было успешно заблокирован на указанное время!```",
        inline=False,
    )
    embed.set_footer(text=f"Дата: {datetime.now()}")
    return embed


def get_user_unban_embed(bot: Client) -> Embed:
    embed = Embed(
        title="Временный мут",
        color=Colour.from_str(bot.config["SUCCESS_COLOR"]),
    )
    embed.add_field(
        name="",
        value=f"```Теперь вам снова разрешено пользоваться сервером!```",
        inline=False,
    )
    embed.set_footer(text=f"Дата: {datetime.now()}")
    return embed


### ВЕЧНЫЙ БАН
def get_user_ban_embed(bot: Client, description: str) -> Embed:
    embed = Embed(
        title="Вечная блокировка",
        color=Colour.from_str(bot.config["ERROR_COLOR"]),
    )
    embed.add_field(
        name="",
        value=f"```Модерация запретила вам посещать сервер на неопределенное время!```",
        inline=False,
    )
    embed.add_field(
        name="",
        value=f"```ПРИЧИНА: {description}```",
        inline=False,
    )
    embed.set_footer(text=f"Дата: {datetime.now()}")
    return embed


def get_user_ban_sent_embed(bot: Client) -> Embed:
    embed = Embed(
        title="Временная блокировка",
        color=Colour.from_str(bot.config["SUCCESS_COLOR"]),
    )
    embed.add_field(
        name="",
        value="```Пользователь было успешно заблокирован!```",
        inline=False,
    )
    embed.set_footer(text=f"Дата: {datetime.now()}")
    return embed
