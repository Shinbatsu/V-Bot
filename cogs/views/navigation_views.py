from discord import ButtonStyle
from discord.ui import View, Button


class NavigationView(
    View,
):
    def __init__(self):
        super().__init__()
        roles_link = Button(
            label="⠀⠀Роли⠀⠀",
            style=ButtonStyle.url,
            url="https://discord.com/channels/711201809372414062/1174660820991475712",
        )
        rank_link = Button(
            label="⠀Профиль",
            style=ButtonStyle.url,
            url="https://discord.com/channels/711201809372414062/1174660701076344852",
        )
        settings_link = Button(
            label="Настройки",
            style=ButtonStyle.url,
            url="https://discord.com/channels/711201809372414062/1171723459039088740",
        )
        self.add_item(roles_link)
        self.add_item(rank_link)
        self.add_item(settings_link)
