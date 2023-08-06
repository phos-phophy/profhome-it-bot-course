from telebot import TeleBot

from .echo import echo_registered_cmd, echo_unregistered_cmd
from .help import help_registered_cmd, help_unregistered_cmd
from .name import change_name_cmd, save_new_name_cmd
from .register import RegisterFilter, cancel_registration_cmd, get_name_cmd, register_cmd, start_cmd

from ..state import ChangeUserInfo, RegisterStepState, RegisteredState


def register_handlers(bot: TeleBot):
    """
    Register handlers and their handler-specific filters.
    """

    # register process handlers
    bot.register_message_handler(callback=start_cmd, pass_bot=True, commands=['start'], state=RegisteredState.non_registered)
    bot.add_custom_filter(RegisterFilter())
    bot.register_message_handler(
        callback=cancel_registration_cmd,
        pass_bot=True,
        content_types=['text'],
        register_reply=False,
        state=RegisterStepState.start
    )
    bot.register_message_handler(
        callback=get_name_cmd,
        pass_bot=True,
        content_types=['text'],
        register_reply=True,
        state=RegisterStepState.start
    )
    bot.register_message_handler(callback=register_cmd, pass_bot=True, content_types=['text'], state=RegisterStepState.select_name)

    # change user info handlers
    bot.register_message_handler(callback=change_name_cmd, pass_bot=True, commands=['change_name'], state=RegisteredState.registered)
    bot.register_message_handler(callback=save_new_name_cmd, pass_bot=True, content_types=['text'], state=ChangeUserInfo.name)

    # help handlers
    bot.register_message_handler(callback=help_registered_cmd, pass_bot=True, commands=['help'], state=RegisteredState.registered)
    bot.register_message_handler(callback=help_unregistered_cmd, pass_bot=True, commands=['help'], state=RegisteredState.non_registered)

    # echo handlers
    bot.register_message_handler(callback=echo_registered_cmd, pass_bot=True, state=RegisteredState.registered)
    bot.register_message_handler(callback=echo_unregistered_cmd, pass_bot=True, state=RegisteredState.non_registered)
