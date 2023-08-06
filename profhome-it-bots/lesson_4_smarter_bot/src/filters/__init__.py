from telebot import TeleBot
from telebot.custom_filters import StateFilter


def register_filters(bot: TeleBot):
    """
    Register common (non-handler-specific) filters.
    NOTE: Handler-specific filter should be registered together with the corresponding handler.
    """

    bot.add_custom_filter(StateFilter(bot))
