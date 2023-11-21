from discord import Embed
from .url_icons import *
from .embed_utils import *

def get_slow_down_embed(cooldown: float) -> Embed:
    embed = Embed(
        title="Подождите!",
    )
    embed.add_field(
        name=f"Нельзя использовать так часто! Попробуйте снова через {cooldown} сек.", value=""
    )
    return embed


def get_pick_rank_embed() -> Embed:
    embed = Embed()
    embed.set_author(
        icon_url=star_url,
        name="Выберите агентов, за которых играете!",
    )
    embed.add_field(
        name="", value="""```Укажите ваше название профиля: NAME#0000. ```""", inline=False
    )
    embed.add_field(
        name="",
        value="""```В случае если указанный вами ник кем-то занят, обратитесь в модерацию.Виновник понесет несовместимое с присутсвием на сервере наказание!```""",
        inline=False,
    )
    embed.add_field(
        name="",
        value="""```В случае если вы решили сменить ваш RIOT аккаунт и хотите обновить ник обратитесь в модерацию.```""",
        inline=False,
    )
    embed.add_field(name="", value=f"""{div}""", inline=False)
    embed.set_footer(
        text="ПРИМЕЧАНИЕ: В целях дополнительной верификации ник можно указать только 1 раз для 1-го аккаунта!",
        icon_url=v_icon_url,
    )
    return embed


def get_different_nicknames_embed(nick: str, repeat_nick: str) -> Embed:
    embed = Embed(
        title="Введенные формы не совпадают!",
    )
    embed.add_field(
        name="```Name:```",
        value=f"""```{nick}```""",
    )
    embed.add_field(
        name="Name repeat:",
        value=f"""```{repeat_nick}```""",
    )
    return embed


def get_already_has_nickname_embed(nick: str) -> Embed:
    embed = Embed(
        title="Ник уже занят!",
    )
    embed.add_field(
        name="",
        value=f"Пользователь {nick} уже использует это имя!",
    )
    return embed


def get_you_got_rank_embed(username: str, rank: str) -> Embed:
    embed = Embed(title="Ваш ранг успешно добавлен!")
    embed.add_field(
        name=f"Поздравляем! {username.capitalize()}! Теперь у вас есть Valorant ранг:",
        value=f"{rank}",
    )
    return embed


def get_you_update_rank_embed(username: str, rank: str) -> Embed:
    embed = Embed(
        title="Ваш ранг успешно обновлен!",
    )
    embed.add_field(name=f"{username.capitalize()}, Теперь ваш Valorant ранг:", value=f"{rank}")
    return embed


def get_cant_get_rank_embed() -> Embed:
    embed = Embed(
        title="Не удалось получить ранг!",
    )
    embed.add_field(name="Произошла ошибка присвоения ранга, попробуйте позже!", value="")
    return embed


def get_cant_update_rank_embed() -> Embed:
    embed = Embed(
        title="Не удалось обновить ранг!",
    )
    embed.add_field(name="Произошла ошибка обновления ранга, попробуйте позже!", value="")
    return embed


def get_cant_update_rank_embed() -> Embed:
    embed = Embed(
        title="Не удалось обновить ранг!",
    )
    embed.add_field(name="У вас пока что нет ранга!", value="")
    return embed


def get_pick_your_agents_embed() -> Embed:
    embed = Embed(
    )
    embed.set_author(
        icon_url=star_url,
        name="Выберите агентов, за которых играете!",
    )
    embed.add_field(
        name="",
        value="```В меню ниже вы можете выбрать агентов, за которых играете, а так же убрать все роли, нажав на кнопку сброса.```",
    )
    embed.set_footer(
        text="Учтите, вы можете выбрать всего одного агента под каждую роль.", icon_url=v_icon_url
    )
    return embed


def get_pick_your_nick_color_embed() -> Embed:
    embed = Embed(
    )
    embed.set_author(
        icon_url=star_url,
        name="Выберите любимый цвет!",
    )
    embed.add_field(
        name="",
        value="```\nПользователи, поддержавшие развитие нашего сервера с помощью буста могут выбрать один из предложенных цветов для своего никнейма. Цвет всегда можно изменить, нажав на другую реакцию.\n```",
    )
    embed.set_footer(text="Ваш любимый цвет станет цветом вашего никнейма.", icon_url=v_icon_url)
    return embed


def get_color_nick_removed_embed() -> Embed:
    embed = Embed(
        title="Изменение цвета",
    )
    embed.add_field(
        name="Ваш цвет ника успешно убран!",
        value="",
    )
    return embed


def get_color_already_selected_embed() -> Embed:
    embed = Embed(
        title="Изменение цвета",
    )
    embed.add_field(
        name="У вас уже есть цвет ника!",
        value="",
    )
    return embed


def get_color_nick_added_embed() -> Embed:
    embed = Embed(
        title="Изменение цвета",
    )
    embed.add_field(
        name="Ваш цвет ника успешно установлен!",
        value="",
    )
    return embed


def get_no_color_to_remove_embed() -> Embed:
    embed = Embed(
        title="Изменение цвета",
    )
    embed.add_field(
        name="У вас должен быть задан цвет для этого действия!",
        value="",
    )
    return embed


def get_agent_added_embed() -> Embed:
    embed = Embed(
        title="Изменение агента",
    )
    embed.add_field(
        name="Ваш агент успешно изменен!",
        value="",
    )
    return embed


def get_agent_removed_embed() -> Embed:
    embed = Embed(
        title="Изменение агента",
    )
    embed.add_field(
        name="Ваш агент успешно убран!",
        value="",
    )
    return embed


def get_agent_already_selected_embed() -> Embed:
    embed = Embed(
        title="Изменение агента",
    )
    embed.add_field(
        name="У вас уже есть агент этого типа!",
        value="",
    )
    return embed
