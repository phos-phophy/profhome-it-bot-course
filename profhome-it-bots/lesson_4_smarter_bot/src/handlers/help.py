from telebot import TeleBot
from telebot.types import Message


def help_registered_cmd(message: Message, bot: TeleBot, user_name: str):
    text = '/help - print this help message\n' \
           '/change_name - change username'

    bot.send_message(chat_id=message.chat.id, text=text)


def help_unregistered_cmd(message: Message, bot: TeleBot):
    text = '/help - print this help message\n' \
           '/start - greet a unregistered user'

    bot.send_message(chat_id=message.chat.id, text=text)
