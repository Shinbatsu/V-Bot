from discord import Embed, Colour
from discord import Client

room_settings_banner = "https://cdn.discordapp.com/attachments/1174664368688996352/1174737742354194454/room_settings.png?ex=6568aec7&is=655639c7&hm=b8fa42f1339ef4ee774af93be7df0b68589df613c9494020d24d3ad4b316e0e1&"


def get_havent_room_embed(bot: Client) -> Embed:
    embed = Embed(
        title="У вас нету комнаты!",
        color=Colour.from_str(bot.config["ERROR_COLOR"]),
    )
    embed.add_field(name=f"Для этого действия сначала необходимо создать комнату.", value="")
    return embed


def get_you_already_has_room_embed(bot: Client) -> Embed:
    embed = Embed(
        title="У вас уже есть комната!",
        color=Colour.from_str(bot.config["INFO_COLOR"]),
    )
    embed.add_field(name="Перейдите ниже, чтобы попасть в неё.", value="")
    return embed


def get_another_user_already_has_room_embed(bot: Client, member_name: str) -> Embed:
    embed = Embed(
        title="Уже владелец!",
        color=Colour.from_str(bot.config["SUCCESS_COLOR"]),
    )
    embed.add_field(name=f"Пользователь {member_name} уже имеет свою комнату!", value="")
    return embed


def get_deleted_embed(bot: Client) -> Embed:
    embed = Embed(
        title="Удаление комнаты",
        color=Colour.from_str(bot.config["SUCCESS_COLOR"]),
    )
    embed.add_field(name="Комната успешно удалена!", value="")
    return embed


def get_room_settings_embed(bot: Client) -> Embed:
    embed = Embed(
        title="Управление приватными каналами",
        color=Colour.from_str(bot.config["INFO_COLOR"]),
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
    embed.set_footer(text="Примечание: Каждый пользователь может иметь только одну комнату!")
    return embed


def get_room_link_embed(bot: Client, url: str) -> Embed:
    embed = Embed(
        title="Приглашение в комнату!",
        color=Colour.from_str(bot.config["SUCCESS_COLOR"]),
    )
    embed.add_field(name="Отправьте ссылку тем, кто должен попасть в комнату:", value="")
    embed.add_field(name=f"{url}", value="")
    embed.set_footer(text="Ссылка действительна 30 дней.")
    return embed


def get_created_room_embed(bot: Client) -> Embed:
    embed = Embed(
        title="Комната создана!",
        color=Colour.from_str(bot.config["SUCCESS_COLOR"]),
    )
    embed.add_field(name="Перейдите ниже, чтобы попасть в неё.", value="")
    return embed


def get_room_closed_embed(bot: Client) -> Embed:
    embed = Embed(
        title="Комната закрыта!",
        color=Colour.from_str(bot.config["SUCCESS_COLOR"]),
    )
    embed.add_field(name="Ваша комната теперь закрыта, даже вы не сможете зайти!", value="")
    return embed


def get_slow_down_embed(bot: Client, cooldown: float) -> Embed:
    embed = Embed(
        title="Подождите!",
        color=Colour.from_str(bot.config["ERROR_COLOR"]),
    )
    embed.add_field(
        name=f"Нельзя создавать комнаты так часто! Попробуйте снова через {cooldown} сек.", value=""
    )
    return embed


def get_room_opened_embed(bot: Client) -> Embed:
    embed = Embed(
        title="Комната открыта!",
        color=Colour.from_str(bot.config["SUCCESS_COLOR"]),
    )
    embed.add_field(name="Ваша комната теперь открыта!", value="")
    return embed


def get_rename_room_embed(bot: Client, new_name: str) -> Embed:
    embed = Embed(
        title="Комната переименована!",
        color=Colour.from_str(bot.config["SUCCESS_COLOR"]),
    )
    embed.add_field(name=f"Теперь ваша комната называется: {new_name}.", value="")
    return embed


def get_change_user_limit_room_embed(bot: Client, user_limit: str) -> Embed:
    embed = Embed(
        title="Количество участников изменено!",
        color=Colour.from_str(bot.config["SUCCESS_COLOR"]),
    )
    embed.add_field(name=f"Теперь ваша комната вмещает: {user_limit} участников.", value="")
    return embed


def get_new_owner_embed(bot: Client, member_name: str) -> Embed:
    embed = Embed(
        title="Новый владелец!",
        color=Colour.from_str(bot.config["SUCCESS_COLOR"]),
    )
    embed.add_field(name=f"Пользователь {member_name} теперь владелец вашей комнаты!", value="")
    return embed


def get_kick_embed(bot: Client, member_name: str) -> Embed:
    embed = Embed(
        title=f"Пользователь выгнан!",
        color=Colour.from_str(bot.config["SUCCESS_COLOR"]),
    )
    embed.add_field(name=f"Пользователь {member_name} изгнан из вашего канала!", value="")
    return embed

def get_kick_self_embed(bot: Client) -> Embed:
    embed = Embed(
        title=f"Нельзя Исключить",
        color=Colour.from_str(bot.config["ERROR_COLOR"]),
    )
    embed.add_field(name=f"Вы не можете выгнать самого себя из канала!", value="")
    return embed

def get_havent_rights_embed(bot: Client, member_name: str) -> Embed:
    embed = Embed(
        title=f"У вас недостаточно прав!",
        color=Colour.from_str(bot.config["SUCCESS_COLOR"]),
    )
    embed.add_field(
        name=f"Вы не являетесь владельцем канала где находится {member_name.name}!", value=""
    )
    return embed


def get_unknown_member_embed(bot: Client, membr_name: str) -> Embed:
    embed = Embed(
        title="Участник не найдет!",
        color=Colour.from_str(bot.config["ERROR_COLOR"]),
    )
    embed.add_field(
        name=f"Пользователь с именем {membr_name} не обнаружен на этом сервере!",
        value="",
    )
    return embed


def get_unknown_member_id_embed(bot: Client, member_id: int) -> Embed:
    embed = Embed(
        title="Участник не найдет!",
        color=Colour.from_str(bot.config["ERROR_COLOR"]),
    )
    embed.add_field(
        name=f"Пользователь с ID:{member_id}, не обнаружен на этом сервере!",
        value="",
    )
    return embed


def get_unknown_value_embed(bot: Client, value: str):
    embed = Embed(
        title="Введено неверное значение!",
        color=Colour.from_str(bot.config["SUCCESS_COLOR"]),
    )
    embed.add_field(
        name=f"Похоже что вы ввели некорректную информацию: {value}",
        value="",
    )
    return embed
