from telebot import TeleBot
from telebot.types import Message
from telebot.handler_backends import BaseMiddleware

from ..state import RegisteredState


class UserNameMiddleware(BaseMiddleware):
    """
    Pass the username as one of the handler arguments.
    """

    def __init__(self, bot: TeleBot):
        super(UserNameMiddleware, self).__init__()
        self._bot = bot
        self.update_types = ['message']

    def pre_process(self, message: Message, data):
        if self._bot.get_state(chat_id=message.chat.id, user_id=message.from_user.id) == RegisteredState.registered.name:
            data['user_name'] = self._bot.retrieve_data(chat_id=message.chat.id, user_id=message.from_user.id).data.get('user_name')

    def post_process(self, message, data, exception):
        pass
