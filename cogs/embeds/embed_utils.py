from discord import Colour
from datetime import datetime
from .url_icons import *


def with_date():
    def decorator(func):
        def wrapper(bot, *args, **kwargs):
            embed = func(bot, *args, **kwargs)
            current_date = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
            embed.set_footer(text=f"Дата: {current_date}")
            return embed
        return wrapper
    return decorator

def info_color():
    def decorator(func):
        def wrapper(bot, *args, **kwargs):
            embed = func(bot, *args, **kwargs)
            embed.color = Colour.from_str(bot.config["INFO_COLOR"])
            return embed
        return wrapper
    return decorator

def error_color():
    def decorator(func):
        def wrapper(bot, *args, **kwargs):
            embed = func(bot, *args, **kwargs)
            embed.color = Colour.from_str(bot.config["ERROR_COLOR"])
            return embed
        return wrapper
    return decorator

def success_color():
    def decorator(func):
        def wrapper(bot, *args, **kwargs):
            embed = func(bot, *args, **kwargs)
            embed.color = Colour.from_str(bot.config["SUCCESS_COLOR"])
            return embed
        return wrapper
    return decorator
