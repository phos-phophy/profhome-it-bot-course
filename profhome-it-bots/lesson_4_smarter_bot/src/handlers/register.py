from telebot import TeleBot
from telebot.custom_filters import AdvancedCustomFilter
from telebot.types import KeyboardButton, Message, ReplyKeyboardMarkup, ReplyKeyboardRemove

from ..state import RegisterStepState, RegisteredState

TEXT_YES = 'Yes'
TEXT_NO = 'No'


def start_cmd(message: Message, bot: TeleBot):
    """
    /start - greet an unregistered users
    """
    bot.send_message(chat_id=message.chat.id, text='Hello! I am a simple test bot created by Artem Kudisov!')

    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add(
        KeyboardButton(text=TEXT_YES),
        KeyboardButton(text=TEXT_NO),
    )

    bot.send_message(chat_id=message.chat.id, text='Would you like to register? (Yes/No)', reply_markup=markup)

    bot.set_state(chat_id=message.chat.id, user_id=message.from_user.id, state=RegisterStepState.start)


class RegisterFilter(AdvancedCustomFilter):
    key = 'register_reply'

    def check(self, update: Message, value: bool) -> bool:
        if value:
            return TEXT_YES.lower() == update.text.lower()
        return TEXT_NO.lower() == update.text.lower()


def cancel_registration_cmd(message: Message, bot: TeleBot):
    """
    Cancel registration process.
    """
    bot.set_state(chat_id=message.chat.id, user_id=message.from_user.id, state=RegisteredState.non_registered)
    bot.send_message(chat_id=message.chat.id, text="I'll be waiting for you later", reply_markup=ReplyKeyboardRemove())


def get_name_cmd(message: Message, bot: TeleBot):
    """
    Start registration process and ask username.
    """
    bot.set_state(chat_id=message.chat.id, user_id=message.from_user.id, state=RegisterStepState.select_name)
    bot.send_message(chat_id=message.chat.id, text='Great! Please tell me your name:', reply_markup=ReplyKeyboardRemove())


def register_cmd(message: Message, bot: TeleBot):
    """
    Register a new user.
    """
    user_name = message.text

    bot.set_state(chat_id=message.chat.id, user_id=message.from_user.id, state=RegisteredState.registered)
    bot.add_data(chat_id=message.chat.id, user_id=message.from_user.id, user_name=user_name)
    bot.send_message(chat_id=message.chat.id, text=f'Nice to meet you, {user_name}!')
