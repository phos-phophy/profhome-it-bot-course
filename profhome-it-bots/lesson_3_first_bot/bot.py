import inspect
import sys

from telebot import TeleBot
from telebot.types import Message

from lesson_3_first_bot.credentials import TOKEN

bot = TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start_cmd(message: Message):
    """
    /start - greet a user
    """
    bot.send_message(chat_id=message.chat.id, text=f'Hello! I am a simple test bot created by Artem Kudisov! Nice to meet you!')


@bot.message_handler(commands=['help'])
def help_cmd(message: Message):
    """
    /help - print this help message
    """
    texts = [doc for _, obj in inspect.getmembers(sys.modules[__name__], inspect.isfunction) if (doc := inspect.getdoc(obj)) is not None]
    bot.send_message(chat_id=message.chat.id, text='\n'.join(texts))


@bot.message_handler(commands=['ping'])
def ping_cmd(message: Message):
    """
    /ping - print 'pong'
    """
    bot.send_message(chat_id=message.chat.id, text='pong')


@bot.message_handler(commands=['pong'])
def pong_cmd(message: Message):
    """
    /pong - print 'ping'
    """
    bot.send_message(chat_id=message.chat.id, text='ping')


@bot.message_handler(commands=['answer'])
def answer_cmd(message: Message):
    """
    /answer - print Answer to the Ultimate Question of Life, the Universe, and Everything
    """
    bot.send_message(chat_id=message.chat.id, text='42 is the Answer to the Ultimate Question of Life, the Universe, and Everything')


@bot.message_handler()
def empty_cmd(message: Message):
    bot.send_message(chat_id=message.chat.id, text='Hmmmm')


bot.infinity_polling()
