from telebot import TeleBot
from telebot.types import Message


def echo_registered_cmd(message: Message, bot: TeleBot, user_name: str):
    bot.send_message(chat_id=message.chat.id, text=f"Sorry, I don't understand you, {user_name}")


def echo_unregistered_cmd(message: Message, bot: TeleBot):
    bot.send_message(chat_id=message.chat.id, text='Hmmmm')
