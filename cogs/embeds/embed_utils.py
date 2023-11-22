from discord import Colour
from datetime import datetime
from .url_icons import *


def with_date():
    def decorator(func):
        def wrapper(*args, **kwargs):
            embed = func(*args, **kwargs)
            current_date = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
            embed.set_footer(text=f"Дата: {current_date}")
            return embed

        return wrapper

    return decorator


def info_color():
    def decorator(func):
        def wrapper(*args, **kwargs):
            embed = func(*args, **kwargs)
            embed.color = Colour.from_str("#11bbbb")
            return embed

        return wrapper

    return decorator


def error_color():
    def decorator(func):
        def wrapper(*args, **kwargs):
            embed = func(*args, **kwargs)
            embed.color = Colour.from_str("#E74D3C")
            return embed

        return wrapper

    return decorator


def success_color():
    def decorator(func):
        def wrapper(*args, **kwargs):
            embed = func(*args, **kwargs)
            embed.color = Colour.from_str("#248046")
            return embed

        return wrapper

    return decorator
