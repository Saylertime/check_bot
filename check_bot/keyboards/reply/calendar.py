# from db_maker import *
# from loader import bot
# from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
# from states.overall import OverallState
#
#
# def show_calendar(bot, chat_id, arrive_or_not):
#     """ Вызывает календарь """
#
#     min_date = datetime.date.today()
#     calendar, step = DetailedTelegramCalendar(locale='ru', min_date=min_date).build()
#     bot.send_message(chat_id,
#                      f"Выберите дату {arrive_or_not}",
#                      reply_markup=calendar)
#
#
# @bot.callback_query_handler(func=DetailedTelegramCalendar.func())
# def cal(c):
#     """ Проверяет колбэк-дату и отправляет пользователя дальше """
#
#     result, key, step = DetailedTelegramCalendar(locale='ru').process(c.data)
#     today = datetime.date.today()
#
#     with bot.retrieve_data(c.from_user.id) as data:
#         if not result and key:
#             bot.edit_message_text(f"Выберите дату {LSTEP[step]}",
#                                   c.message.chat.id,
#                                   c.message.message_id,
#                                   reply_markup=key)
#
#         elif result is not None and data['date1'] == 0:
#             bot.send_message(c.message.chat.id, 'И дату выезда')
#             bot.edit_message_text(f"Вы выбрали {result} ",
#                                               c.message.chat.id,
#                                               c.message.message_id)
#             show_calendar(bot, c.message.chat.id, 'выезда')
#             data['date1'] = result
#
#         else:
#             if data['state'] == 'OverallState':
#                 bot.set_state(c.message.from_user.id, OverallState.minimum)
#
#             bot.edit_message_text("Введи минимальную цену: ",
#                                       c.message.chat.id,
#                                       c.message.message_id)
#             data['date2'] = result












from db_maker import *
from loader import bot
from telegram_bot_calendar import DetailedTelegramCalendar
from keyboards.reply.create_markup import create_markup
from states.reminders import ReminderState


def show_calendar(bot, chat_id, arrive_or_not, min_date):
    """ Вызывает календарь """

    max_date = datetime.date.today()
    calendar, step = DetailedTelegramCalendar(locale='ru', min_date=min_date, max_date=max_date).build()
    bot.send_message(chat_id,
                     f"Выберите дату",
                     reply_markup=calendar)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func())
def cal(c):
    """ Проверяет колбэк-дату и отправляет пользователя дальше """

    result, key, step = DetailedTelegramCalendar(locale='ru').process(c.data)
    bot.set_state(c.message.from_user.id, ReminderState.final)

    with bot.retrieve_data(c.from_user.id) as data:
        if not result and key:
            bot.edit_message_text(f"Выберите дату",
                                  c.message.chat.id,
                                  c.message.message_id,
                                  reply_markup=key)

        elif result is not None and data.get('first') is None:
            bot.edit_message_text(f"Вы выбрали {result}.\nТеперь выберите дату окончания.",
                                  c.message.chat.id,
                                  c.message.message_id)
            data['first'] = result
            show_calendar(bot, c.message.chat.id, '', result)

        elif result is not None and data.get('first') is not None and data.get('second') is None:
            bot.edit_message_text(f"Вы выбрали {data['first']} - {result}.",
                                  c.message.chat.id,
                                  c.message.message_id)
            data['second'] = result
            bot.send_message(c.message.chat.id, f"Вы выбрали период с {data['first']} по {data['second']}.")
            bot.set_state(c.from_user.id, ReminderState.final)
            buttons = [('Посмотреть статистику', 'statistics')]
            markup = create_markup(buttons)
            bot.send_message(c.from_user.id, 'Посмотреть статистику', reply_markup=markup)


