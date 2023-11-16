from discord import Embed, Colour
from discord import Client

v_icon_url = "https://cdn.discordapp.com/attachments/1174664368688996352/1174669493683888148/v_icon.png?ex=65686f37&is=6555fa37&hm=f61d317ecfa5e72fb839db3d684f2add8c592c4887825d6f0382974bd232de6b&"

agent_roles_banner = "https://cdn.discordapp.com/attachments/1174664368688996352/1174735279467278397/roles.png?ex=6568ac7c&is=6556377c&hm=4b0c4dd896afc2f427ade83573ffe61ce64ee6886f0190230945a4f254556a14&"
nick_color_banner = "https://cdn.discordapp.com/attachments/1174664368688996352/1174736823453487205/nick_color.png?ex=6568adec&is=655638ec&hm=6dfe5b66d72df18e40d61e50fbe25d4bf135603abd9a4b971c387feb0bd8d51b&"
dot_url = "https://cdn.discordapp.com/attachments/1174664368688996352/1174744429861552168/dot.png?ex=6568b501&is=65564001&hm=e91241e4824b9a27827330ede6807148affc84826a4b039a8632fd5e4c3029db&"
star_url = "https://cdn.discordapp.com/attachments/1174664368688996352/1174744769692450916/star.png?ex=6568b552&is=65564052&hm=9cb96a2855f02f5dbd56d733e98a58abf52052329f6ab36fd9bd2e23cccfad81&"


def get_pick_your_agents_embed(bot: Client) -> Embed:
    embed = Embed(
        color=Colour.from_str(bot.config["INFO_COLOR"]),
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


def get_pick_your_nick_color_embed(bot: Client) -> Embed:
    embed = Embed(
        color=Colour.from_str(bot.config["INFO_COLOR"]),
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


def get_color_nick_removed_embed(bot: Client) -> Embed:
    embed = Embed(
        title="Изменение цвета",
        color=Colour.from_str(bot.config["SUCCESS_COLOR"]),
    )
    embed.add_field(
        name="Ваш цвет ника успешно убран!",
        value="",
    )
    return embed
def get_color_already_selected_embed(bot: Client) -> Embed:
    embed = Embed(
        title="Изменение цвета",
        color=Colour.from_str(bot.config["ERROR_COLOR"]),
    )
    embed.add_field(
        name="У вас уже есть цвет ника!",
        value="",
    )
    return embed

def get_color_nick_added_embed(bot: Client) -> Embed:
    embed = Embed(
        color=Colour.from_str(bot.config["SUCCESS_COLOR"]),
    )
    embed.add_field(
        title="Изменение цвета",
        name="Ваш цвет ника успешно установлен!",
        value="",
    )
    return embed

def get_no_color_to_remove_embed(bot: Client) -> Embed:
    embed = Embed(
        title="Изменение цвета",
        color=Colour.from_str(bot.config["ERROR_СOLOR"]),
    )
    embed.add_field(
        name="У вас должен быть задан цвет для этого действия!",
        value="",
    )
    return embed

def get_agent_added_embed(bot: Client) -> Embed:
    embed = Embed(
        title="Изменение агента",
        color=Colour.from_str(bot.config["SUCCESS_COLOR"]),
    )
    embed.add_field(
        name="Ваш агент успешно изменен!",
        value="",
    )
    return embed


def get_agent_removed_embed(bot: Client) -> Embed:
    embed = Embed(
        title="Изменение агента",
        color=Colour.from_str(bot.config["SUCCESS_COLOR"]),
    )
    embed.add_field(
        name="Ваш агент успешно убран!",
        value="",
    )
    return embed


def get_agent_already_selected_embed(bot: Client) -> Embed:
    embed = Embed(
        title="Изменение агента",
        color=Colour.from_str(bot.config["ERROR_COLOR"]),
    )
    embed.add_field(
        name="У вас уже есть агент этого типа!",
        value="",
    )
    return embed
