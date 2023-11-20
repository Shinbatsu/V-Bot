from discord import ButtonStyle
from discord.ui import View, Button
from ..embeds.navigation_embed import *

class NavigationView(
    View,
):
    def __init__(self, bot, rank_room_url, roles_room_url, settinigs_room_url):
        super().__init__(timeout=None)
        self.bot = bot
        
        roles_link = Button(label="⠀⠀Роли⠀⠀", style=ButtonStyle.link, url=roles_room_url)
        rank_link = Button(label="⠀Профиль", style=ButtonStyle.link, url=rank_room_url)
        # settings_link = Button(label="Настройки", style=ButtonStyle.link, url=settinigs_room_url)
        self.add_item(roles_link)
        self.add_item(rank_link)
        # self.add_item(settings_link)
