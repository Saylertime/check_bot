from loader import bot
import handlers
from telebot.custom_filters import StateFilter
from utils.set_bot_commands import set_default_commands
from config_data import config
import threading
from flask import Flask, request
import requests
import telebot
import time


app = Flask(__name__)

WEBHOOK_URL = 'https://glinkin.pro'
BOT_TOKEN = config.BOT_TOKEN

@app.route('/webhook_check_bot', methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
    bot.process_new_updates([update])
    return 'ok', 200

def set_webhook():
    response = requests.get(f'https://api.telegram.org/bot{BOT_TOKEN}/setWebhook?url={WEBHOOK_URL}/webhook_check_bot')
    print(response.json())

def webhook_thread():
    for i in range(1, 4):
        set_webhook()
        time.sleep(10)
set_webhook()

def delete_webhook():
    response = requests.get(f'https://api.telegram.org/bot{BOT_TOKEN}/deleteWebhook')
    print(response.json())

if __name__ == "__main__":
    delete_webhook()
    bot.add_custom_filter(StateFilter(bot))
    set_default_commands(bot)
    # bot.infinity_polling()

    webhook_thread = threading.Thread(target=webhook_thread)
    webhook_thread.start()
    app.run(host='0.0.0.0', port=5007)
