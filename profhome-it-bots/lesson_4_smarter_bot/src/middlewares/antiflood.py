from typing import Any

from telebot import BaseMiddleware, TeleBot
from telebot.handler_backends import CancelUpdate
from telebot.types import Message

from ..state import RegisteredState


class AntifloodMiddleware(BaseMiddleware):
    def __init__(self, bot: TeleBot, limit: float):
        super(AntifloodMiddleware, self).__init__()
        self._bot = bot
        self._limit = limit
        self.update_types = ['message']

    def pre_process(self, message: Message, data: Any):
        user_data = self._bot.retrieve_data(chat_id=message.chat.id, user_id=message.from_user.id).data

        if user_data is None:
            self._bot.set_state(chat_id=message.chat.id, user_id=message.from_user.id, state=RegisteredState.non_registered)
            self._bot.add_data(chat_id=message.chat.id, user_id=message.from_user.id, last_message=message.date)
            return

        last_message = user_data.get('last_message', None)

        self._bot.add_data(chat_id=message.chat.id, user_id=message.from_user.id, last_message=message.date)

        if last_message is not None and message.date - last_message < self._limit:
            self._bot.send_message(message.chat.id, 'You are sending messages too often! Try later!')
            return CancelUpdate()

    def post_process(self, message: Message, data, exception):
        pass

    @classmethod
    def from_config(cls, bot: TeleBot, config: dict) -> 'AntifloodMiddleware':
        return cls(bot=bot, limit=config['limit'])
