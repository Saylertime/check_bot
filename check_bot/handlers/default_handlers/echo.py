from loader import bot

@bot.message_handler(state=None)
def bot_echo(message) -> None:
    """ Вызывается, когда пользователь без состояния вводит несуществующую команду """

    bot.reply_to(
        message, f"Такой команды нет: {message.text}\n"
                 f"Нажмите /start, чтобы добавить ссылку на чек за этот месяц"
    )
