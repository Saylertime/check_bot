from loader import bot
from utils.sheets import get_data_from_sheet, new_list
from states import CheckState
import re


@bot.message_handler(commands=['start'])
def start_message(message):
    if get_data_from_sheet(message.from_user.username):
        msg = f"Закинь сюда ссылку на чек. Больше ничего не надо — ни имени, ни месяца"
        bot.send_message(message.chat.id, msg)
        bot.set_state(message.from_user.id, state=CheckState.check)
    else:
        bot.send_message(message.chat.id, 'Тебя нет в базе данных... Обратись к Александру, чтобы он порешал')


@bot.message_handler(state=CheckState.check)
def upload_link(message):
    if contains_ru_domain(message.text):
        full_name = get_data_from_sheet(message.from_user.username)
        new_list(full_name, message.text)
        bot.delete_state(message.from_user.id)
        bot.send_message(message.from_user.id, 'Спасибо, всё получилось')
    else:
        bot.send_message(message.from_user.id, 'Это точно ссылка? Не вижу в ней .ru')


def contains_ru_domain(url):
    ru_pattern = re.compile(r'\.ru\b', re.IGNORECASE)
    return re.search(ru_pattern, url) is not None