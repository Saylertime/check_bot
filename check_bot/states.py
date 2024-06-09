from telebot.handler_backends import State, StatesGroup

class CheckState(StatesGroup):
    """ Класс со всеми необходимыми состояниями """

    check = State()
