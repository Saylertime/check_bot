from telebot import types

def create_markup(buttons):
    """ Создает кнопки для ответа """

    markup = types.InlineKeyboardMarkup()
    for text, callback_data in buttons:
        markup.add(types.InlineKeyboardButton(text=text, callback_data=callback_data))
    return markup
