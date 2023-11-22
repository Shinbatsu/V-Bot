from discord import Embed, Colour
from datetime import datetime
from .url_icons import *
from .embed_utils import *


@info_color()
def get_slow_down_embed(cooldown: float) -> Embed:
    embed = Embed(
        title="Подождите!",
    )
    embed.add_field(
        name=f"Нельзя использовать так часто! Попробуйте снова через {cooldown} сек.", value=""
    )
    return embed


@info_color()
def get_ticket_embed() -> Embed:
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
def get_report_sent_embed() -> Embed:
    embed = Embed()
    embed.set_author(icon_url=star_url, name=" Оставьте жалобу на участника")
    embed.add_field(
        name="",
        value="""```Наши модераторы в кратчайшие сроки постараются проверить вашу жалому, нарушитель будет наказан!```""",
        inline=False,
    )
    embed.set_footer(
        text="Иногда для проверки жалобы могут потребоваться скриншоты, видео или другая информация."
    )
    return embed


@error_color()
def get_self_report_embed() -> Embed:
    embed = Embed(
        title="Попытка саморепорта!",
    )
    embed.add_field(
        name="",
        value="""```Похоже что вы указали собственный ID, в качетве того, \nкто по вашему мнению является виноватым! Ваш запрос был отклонен!```""",
        inline=False,
    )
    return embed


@info_color()
def get_report_info_embed(author: str, reported_user: str, description: str) -> Embed:
    embed = Embed(
        title="Cоздана новая жалоба на пользователя",
    )
    embed.add_field(
        name=f"""{dot}Автор: {author}""",
        value="",
        inline=False,
    )
    embed.add_field(
        name=f"""```{dot}Виновник: {reported_user}```""",
        value="",
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
@success_color()
def get_report_was_resolved_embed(jump_url, moderator_name) -> Embed:
    embed = Embed(
        title="Жалоба закрыта",
    )
    embed.add_field(
        name="",
        value=f"""[Заявка]({jump_url}) ```была разрешена модератором {moderator_name}.```""",
        inline=False,
    )
    embed.set_footer(text=f"Дата: {datetime.now()}")
    return embed


### ПРЕДУПРЕЖДЕНИЕ
@error_color()
def get_user_warn_embed(description: str) -> Embed:
    embed = Embed(
        title="Замечание",
    )
    embed.add_field(name="", value=f"```ПРИЧИНА: {description.capitalize()}```")
    embed.set_footer(text=f"Дата: {datetime.now()}")
    return embed


@success_color()
def get_user_warn_sent_embed() -> Embed:
    embed = Embed(
        title="Замечание",
    )
    embed.add_field(
        name="",
        value="```Замечание пользователю было успешно отправлено!```",
        inline=False,
    )
    embed.set_footer(text=f"Дата: {datetime.now()}")
    return embed


### КИК
@error_color()
def get_user_kick_embed(description: str) -> Embed:
    embed = Embed(
        title="Кик",
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


@success_color()
def get_user_kick_sent_embed() -> Embed:
    embed = Embed(
        title="Кик",
    )
    embed.add_field(
        name="",
        value="```Пользователь был успешно кикнут!```",
        inline=False,
    )
    embed.set_footer(text=f"Дата: {datetime.now()}")

    return embed


### ВРЕМЕННЫЙ МУТ
@error_color()
def get_user_temp_mute_embed(description: str, time: int) -> Embed:
    embed = Embed(
        title="Временный мут",
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


@success_color()
def get_user_temp_mute_sent_embed() -> Embed:
    embed = Embed(
        title="Временный мут",
    )
    embed.add_field(
        name="",
        value="```Пользователю было успешно запрещено говорить!```",
        inline=False,
    )
    embed.set_footer(text=f"Дата: {datetime.now()}")
    return embed


@success_color()
def get_user_unmute_embed() -> Embed:
    embed = Embed(
        title="Временный мут",
    )
    embed.add_field(
        name="",
        value=f"```Теперь вам снова разрешено использовать голосовые сообщения!```",
        inline=False,
    )
    embed.set_footer(text=f"Дата: {datetime.now()}")
    return embed
    ### ВРЕМЕННЫЙ ЗАПРЕТ ПЕЧАТИ


@error_color()
def get_user_temp_stop_typing_embed(description: str, time: int) -> Embed:
    embed = Embed(
        title="Временный мут",
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


@success_color()
def get_user_temp_stop_typing_sent_embed() -> Embed:
    embed = Embed(
        title="Временный мут",
    )
    embed.add_field(
        name="",
        value="```Пользователю было запрещено использовать текстовый чат!```",
        inline=False,
    )
    embed.set_footer(text=f"Дата: {datetime.now()}")
    return embed


@success_color()
def get_user_temp_unstop_typing_embed() -> Embed:
    embed = Embed(
        title="Временный мут",
    )
    embed.add_field(
        name="",
        value=f"```Теперь вам снова разрешено использовать текстовый чат!```",
        inline=False,
    )
    embed.set_footer(text=f"Дата: {datetime.now()}")
    return embed


### ВРЕМЕННЫЙ БАН
@error_color()
def get_user_temp_ban_embed(description: str, time: int) -> Embed:
    embed = Embed(
        title="Временная блокировка",
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


@success_color()
def get_user_temp_ban_sent_embed() -> Embed:
    embed = Embed(
        title="Временная блокировка",
    )
    embed.add_field(
        name="",
        value="```Пользователь было заблокирован на указанное время!```",
        inline=False,
    )
    embed.set_footer(text=f"Дата: {datetime.now()}")
    return embed


@success_color()
def get_user_unban_embed() -> Embed:
    embed = Embed(
        title="Временный мут",
    )
    embed.add_field(
        name="",
        value=f"```Теперь вам снова разрешено пользоваться сервером!```",
        inline=False,
    )
    embed.set_footer(text=f"Дата: {datetime.now()}")
    return embed


### ВЕЧНЫЙ БАН
@error_color()
def get_user_ban_embed(description: str) -> Embed:
    embed = Embed(
        title="Вечная блокировка",
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


@success_color()
def get_user_ban_sent_embed() -> Embed:
    embed = Embed(
        title="Временная блокировка",
    )
    embed.add_field(
        name="",
        value="```Пользователь было успешно заблокирован!```",
        inline=False,
    )
    embed.set_footer(text=f"Дата: {datetime.now()}")
    return embed
