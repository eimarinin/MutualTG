# main.py
import logging
from telebot import TeleBot
from config import config
from sheets.client import SheetsClient
from bot.handlers import register_handlers

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

bot = TeleBot(config.BOT_TOKEN)
sheets = SheetsClient()

def main():
    register_handlers(bot, sheets)
    logging.info("Бот запущен")
    bot.infinity_polling(skip_pending=True, timeout=20, long_polling_timeout=20)

if __name__ == "__main__":
    main()