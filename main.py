# main.py
import logging
import time
import os
import threading
from flask import Flask
from telebot import TeleBot
from config import config
from sheets.client import SheetsClient
from bot.handlers import register_handlers

# Логирование
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Flask для Render health-check (отвечает "OK" на /)
app = Flask(__name__)

@app.route('/')
def health_check():
    return 'OK', 200  # Render увидит это и не убьёт сервис

def run_flask():
    port = int(os.environ.get('PORT', 10000))  # Render PORT по умолчанию 10000
    app.run(host='0.0.0.0', port=port, debug=False)

def run_bot():
    bot = TeleBot(config.BOT_TOKEN)
    sheets = SheetsClient()
    register_handlers(bot, sheets)
    
    logging.info("Бот запущен — стабильный polling с рестартом")
    
    retry_count = 0
    max_retries = 5
    
    while True:
        try:
            bot.infinity_polling(
                skip_pending=True,
                timeout=30,
                long_polling_timeout=30
            )
            retry_count = 0
        except Exception as e:
            retry_count += 1
            logging.error(f"Polling упал (попытка {retry_count}/{max_retries}): {e}")
            if retry_count >= max_retries:
                logging.warning("Много ошибок — пауза 5 мин...")
                time.sleep(300)
                retry_count = 0
            else:
                time.sleep(60)

def main():
    # Запускаем Flask в фоне (для Render порта)
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    logging.info(f"Flask health-server запущен на порту {os.environ.get('PORT', 10000)}")
    
    # Запускаем бота в фоне
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    
    # Держим основной поток живым
    while True:
        time.sleep(60)
        logging.info("Сервис активен — Flask и бот работают")

if __name__ == "__main__":
    main()