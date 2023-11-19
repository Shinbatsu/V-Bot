from discord import Embed, Colour
from discord import Client
from .url_icons import *
from .embed_utils import *


@error_color()
def get_havent_room_embed(bot: Client) -> Embed:
    embed = Embed(
        title="У вас нету комнаты!",
    )
    embed.add_field(name=f"Для этого действия сначала необходимо создать комнату.", value="")
    return embed


@info_color()
def get_you_already_has_room_embed(bot: Client) -> Embed:
    embed = Embed()
    embed.set_author(
        icon_url=alert_url,
        name="Уже есть комната",
        inline=False,
    )
    embed.add_field(
        name="",
        value=f"""{div}""",
        inline=False,
    )
    embed.add_field(
        name="Перейдите ниже, чтобы попасть в неё.",
        value="",
        inline=False,
    )
    return embed


@success_color()
def get_another_user_already_has_room_embed(bot: Client, member_name: str) -> Embed:
    embed = Embed(
        title="Уже владелец",
    )
    embed.add_field(name=f"Пользователь {member_name} уже имеет свою комнату!", value="")
    return embed


@success_color()
def get_room_deleted_embed(bot: Client) -> Embed:
    embed = Embed(
        title="Удаление комнаты",
    )
    embed.add_field(name="Комната успешно удалена!", value="")
    return embed


@success_color()
def get_room_upped_embed(bot: Client) -> Embed:
    embed = Embed(
        title="Поднятие комнаты",
    )
    embed.add_field(name="Комната успешно поднята!", value="")
    return embed


@info_color()
def get_room_settings_embed(bot: Client) -> Embed:
    embed = Embed(
        title="Управление приватными каналами",
    )
    embed.add_field(
        name="<:custom_lock:1173271460970758204> - ```Заблокировать вход в канал```",
        value="",
        inline=False,
    )
    embed.add_field(
        name="<:kick:1173271463244087336> - ```Исключить пользователя из канала```",
        value="",
        inline=False,
    )
    embed.add_field(
        name="<:slots:1173271467060904050> - ```Изменить количество слотов в канале```",
        value="",
        inline=False,
    )
    embed.add_field(
        name="<:change_owner:1173271455786602526> - ```Изменить владельца канала```",
        value="",
        inline=False,
    )
    embed.add_field(
        name="<:rename:1173271464699498677> - ```Изменить название канала```",
        value="",
        inline=False,
    )
    embed.add_field(name="CREATE ROOM - ```Создать комнату```", value="", inline=False)
    embed.add_field(name="DELETE - ```Удалить комнату```", value="", inline=False)
    embed.add_field(name="UP - ```Поднять комнату```", value="", inline=False)
    embed.add_field(
        name="", value=f"{div}", inline=False
    )
    embed.add_field(
        name="", value="Примечание: Каждый пользователь может иметь только одну комнату!", inline=False
    )

    return embed


@success_color()
def get_room_link_embed(bot: Client, url: str) -> Embed:
    embed = Embed(
        title="Приглашение в комнату",
    )
    embed.add_field(
        name="Отправьте ссылку тем, кто должен попасть в комнату:", value="", inline=False
    )
    embed.add_field(name="", value=f"Cсылка: {url}", inline=False)
    embed.set_footer(text="Ссылка действительна 30 дней.")
    return embed


@success_color()
def get_created_room_embed(bot: Client) -> Embed:
    embed = Embed(
        title="Комната создана",
    )
    embed.add_field(name="Перейдите ниже, чтобы попасть в неё.", value="")
    return embed


@success_color()
def get_room_closed_embed(bot: Client) -> Embed:
    embed = Embed(
        title="Комната закрыта",
    )
    embed.add_field(name="Ваша комната теперь закрыта, даже вы не сможете зайти!", value="")
    return embed


@error_color()
def get_slow_down_embed(bot: Client, cooldown: float) -> Embed:
    embed = Embed(
        title="Подождите!",
    )
    embed.add_field(
        name=f"Нельзя создавать комнаты так часто! Попробуйте снова через {cooldown} сек.", value=""
    )
    return embed


@success_color()
def get_room_opened_embed(bot: Client) -> Embed:
    embed = Embed(
        title="Комната открыта!",
    )
    embed.add_field(name="Ваша комната теперь открыта!", value="")
    return embed


@success_color()
def get_rename_room_embed(bot: Client, new_name: str) -> Embed:
    embed = Embed(
        title="Комната переименована!",
    )
    embed.add_field(name=f"Теперь ваша комната называется: {new_name}.", value="")
    return embed


@success_color()
def get_change_user_limit_room_embed(bot: Client, user_limit: str) -> Embed:
    embed = Embed(
        title="Количество участников изменено!",
    )
    embed.add_field(name=f"Теперь ваша комната вмещает: {user_limit} участников.", value="")
    return embed


@success_color()
def get_new_owner_embed(bot: Client, member_name: str) -> Embed:
    embed = Embed(
        title="Новый владелец!",
    )
    embed.add_field(name=f"Пользователь {member_name} теперь владелец вашей комнаты!", value="")
    return embed


@success_color()
def get_kick_embed(bot: Client, member_name: str) -> Embed:
    embed = Embed(
        title=f"Пользователь выгнан!",
    )
    embed.add_field(name=f"Пользователь {member_name} изгнан из вашего канала!", value="")
    return embed


@error_color()
def get_kick_self_embed(bot: Client) -> Embed:
    embed = Embed(
        title=f"Нельзя Исключить",
    )
    embed.add_field(name=f"Вы не можете выгнать самого себя из канала!", value="")
    return embed


@success_color()
def get_havent_rights_embed(bot: Client, member_name: str) -> Embed:
    embed = Embed(
        title=f"У вас недостаточно прав!",
    )
    embed.add_field(
        name=f"Вы не являетесь владельцем канала где находится {member_name.name}!", value=""
    )
    return embed


@error_color()
def get_unknown_member_embed(bot: Client, membr_name: str) -> Embed:
    embed = Embed(
        title="Участник не найдет!",
    )
    embed.add_field(
        name=f"Пользователь с именем {membr_name} не обнаружен на этом сервере!",
        value="",
    )
    return embed


@error_color()
def get_unknown_member_id_embed(bot: Client, member_id: int) -> Embed:
    embed = Embed(
        title="Участник не найдет!",
    )
    embed.add_field(
        name=f"Пользователь с ID:{member_id}, не обнаружен на этом сервере!",
        value="",
    )
    return embed


@success_color()
def get_unknown_value_embed(bot: Client, value: str):
    embed = Embed(
        title="Введено неверное значение!",
    )
    embed.add_field(
        name=f"Похоже что вы ввели некорректную информацию: {value}",
        value="",
    )
    return embed
