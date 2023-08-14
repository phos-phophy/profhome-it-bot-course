from telebot import TeleBot

from .antiflood import AntifloodMiddleware
from .user_name import UserNameMiddleware


def register_middlewares(bot: TeleBot, config: dict):
    """
    Register common middlewares.
    """

    antiflood_mw = AntifloodMiddleware.from_config(bot, config.get('antiflood', {}))
    user_name_mw = UserNameMiddleware(bot)

    bot.setup_middleware(antiflood_mw)
    bot.setup_middleware(user_name_mw)
