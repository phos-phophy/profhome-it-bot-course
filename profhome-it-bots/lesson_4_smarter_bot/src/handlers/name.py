from telebot import TeleBot
from telebot.types import Message

from ..state import ChangeUserInfo, RegisteredState


def change_name_cmd(message: Message, bot: TeleBot, user_name: str):
    bot.set_state(chat_id=message.chat.id, user_id=message.from_user.id, state=ChangeUserInfo.name)
    bot.send_message(chat_id=message.chat.id, text='Ok, please tell me your new name:')


def save_new_name_cmd(message: Message, bot: TeleBot):
    user_name = message.text

    bot.set_state(chat_id=message.chat.id, user_id=message.from_user.id, state=RegisteredState.registered)
    bot.add_data(chat_id=message.chat.id, user_id=message.from_user.id, user_name=user_name)
    bot.send_message(chat_id=message.chat.id, text=f'All done, {user_name}!')
