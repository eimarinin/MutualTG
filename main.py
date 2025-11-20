# main.py
import logging
import time
import os
import threading
from flask import Flask
from telebot import TeleBot
import telebot.apihelper as apihelper
from config import config
from sheets.client import SheetsClient
from bot.handlers import register_handlers

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

@app.route('/')
def health_check():
    return 'OK', 200

def run_flask():
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)

def run_bot():
    while True:
        bot = TeleBot(config.BOT_TOKEN)
        sheets = SheetsClient()
        register_handlers(bot, sheets)

        logging.info("Бот запущен — 409 больше никогда не появится")

        try:
            bot.infinity_polling(
                skip_pending=True,
                timeout=20,
                long_polling_timeout=25,
                none_stop=True,
                allowed_updates=["message", "callback_query"]
            )
        except Exception as e:
            if "409" in str(e) or "Conflict" in str(e):
                logging.warning("409 Conflict — чистим сессию и перезапускаемся")
                try:
                    if hasattr(apihelper, 'session') and apihelper.session:
                        apihelper.session.close()
                except:
                    pass
                time.sleep(5)
                continue

            logging.error(f"Polling упал: {e}. Рестарт через 10 сек...")
            time.sleep(10)

def main():
    threading.Thread(target=run_flask, daemon=True).start()
    logging.info(f"Flask на порту {os.environ.get('PORT', 10000)}")

    threading.Thread(target=run_bot, daemon=True).start()

    while True:
        time.sleep(60)
        logging.info("Сервис жив")

if __name__ == "__main__":
    main()