from telebot.handler_backends import State, StatesGroup


class RegisteredState(StatesGroup):
    registered = State()
    non_registered = State()


class RegisterStepState(StatesGroup):
    start = State()
    select_name = State()


class ChangeUserInfo(StatesGroup):
    name = State()
