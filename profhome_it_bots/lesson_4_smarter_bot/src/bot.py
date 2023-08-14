from argparse import Namespace

from telebot import TeleBot

from .utils import get_token, read_config
from .handlers import register_handlers
from .middlewares import register_middlewares
from .filters import register_filters


def setup_bot(args: Namespace) -> TeleBot:
    """
    Initialize bot and register filters, middlewares and handlers.
    """

    config = read_config(args.config)
    token = get_token(args.token)

    bot = TeleBot(token, use_class_middlewares=True)

    register_filters(bot)
    register_middlewares(bot, config.get('middlewares', {}))
    register_handlers(bot)

    return bot
