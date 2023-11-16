from discord import Embed, Colour
from discord import Client

v_icon_url = "https://cdn.discordapp.com/attachments/1174664368688996352/1174669493683888148/v_icon.png?ex=65686f37&is=6555fa37&hm=f61d317ecfa5e72fb839db3d684f2add8c592c4887825d6f0382974bd232de6b&"

valorant_ranking_banner = "https://cdn.discordapp.com/attachments/1174664368688996352/1174751128794173501/valorant_ranking.png?ex=6568bb3e&is=6556463e&hm=99997ad709171903476eda9c1a55089b34f5d09df57d218bdd0d7f38448c7e69&"
nick_color_banner = "https://cdn.discordapp.com/attachments/1174664368688996352/1174736823453487205/nick_color.png?ex=6568adec&is=655638ec&hm=6dfe5b66d72df18e40d61e50fbe25d4bf135603abd9a4b971c387feb0bd8d51b&"
dot_url = "https://cdn.discordapp.com/attachments/1174664368688996352/1174744429861552168/dot.png?ex=6568b501&is=65564001&hm=e91241e4824b9a27827330ede6807148affc84826a4b039a8632fd5e4c3029db&"
star_url = "https://cdn.discordapp.com/attachments/1174664368688996352/1174744769692450916/star.png?ex=6568b552&is=65564052&hm=9cb96a2855f02f5dbd56d733e98a58abf52052329f6ab36fd9bd2e23cccfad81&"


def get_pick_rank_embed(bot: Client) -> Embed:
    embed = Embed(
        title="Получить ваш Valorant ранг",
        color=Colour.from_str(bot.config["INFO_COLOR"]),
    )
    embed.add_field(
        name="",
        value="""```Укажите ваше название профиля: NAME#0000. ```""",inline=False
    )
    embed.add_field(
        name="",
        value="""```В случае если указанный вами ник кем-то занят, обратитесь в модерацию.Виновник понесет несовместимое с присутсвием на сервере наказание!```""",inline=False
    )
    embed.add_field(
        name="",
        value="""```В случае если вы решили сменить ваш RIOT аккаунт и хотите обновить ник обратитесь в модерацию.```""",inline=False
    )
    embed.set_footer(
        text="ПРИМЕЧАНИЕ: В целях дополнительной верификации ник можно указать только 1 раз для 1-го аккаунта!",
        icon_url=v_icon_url,
    )
    return embed


def get_different_nicknames_embed(bot: Client, nick: str, repeat_nick: str) -> Embed:
    embed = Embed(
        title="Введенные формы не совпадают!",
        color=Colour.from_str(bot.config["ERROR_COLOR"]),
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


def get_already_has_nickname_embed(bot: Client, nick: str) -> Embed:
    embed = Embed(
        title="Ник уже занят!",
        color=Colour.from_str(bot.config["ERROR_COLOR"]),
    )
    embed.add_field(
        name="",
        value=f"Пользователь {nick} уже использует это имя!",
    )
    return embed


def get_you_got_rank_embed(bot: Client, user_name: str, rank: str) -> Embed:
    embed = Embed(title="Ваш ник успешно добавлен!", color=Colour.from_str(bot.config["SUCCESS_COLOR"]),)
    embed.add_field(name=f"Поздравляем! {user_name.capitalize()}! Теперь у вас есть Valorant ранг:", value=f"{rank}")
    return embed
def get_cant_get_rank_embed(bot:Client) -> Embed:        
    embed = Embed(title="Не удалось получить ранг!", color=Colour.from_str(bot.config["ERROR_COLOR"]),)
    embed.add_field(name="Произошла ошибка присвоения ранга, попробуйте позже!", value="")
    return embed