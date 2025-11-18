# main.py
import telebot
from telebot.types import ReplyKeyboardRemove
from config import Config
from sheets.client import SheetsClient
import logging

# Логирование
logging.basicConfig(level=logging.INFO)

bot = telebot.TeleBot(Config.BOT_TOKEN)
sheets = SheetsClient()

@bot.message_handler(commands=['start'])
def start(message):
    text = (
        "Привет! Я бот взаимных подписок Telegram\n\n"
        "Отправь ссылку на свой канал (t.me/xxx или @xxx)\n"
        "Я добавлю его в базу и начну искать взаимки\n\n"
        "Требования:\n"
        "• От 50 живых подписчиков\n"
        "• Без 18+, политики, крипты"
    )
    bot.send_message(message.chat.id, text, reply_markup=ReplyKeyboardRemove())

@bot.message_handler(func=lambda m: True)
def save_channel(message):
    link = message.text.strip()
    user = message.from_user
    username = f"@{user.username}" if user.username else "без_юзернейма"

    if not ("t.me" in link or link.startswith("@")):
        bot.reply_to(message, "Неправильная ссылка. Пример: t.me/mychannel")
        return

    if sheets.add_channel(user.id, username, link):
        bot.reply_to(message, 
            "Готово! Твой канал в очереди на взаимки\n"
            "Сейчас в базе 300+ каналов — скоро начнём подписываться друг на друга"
        )
    else:
        bot.reply_to(message, "Ошибка записи, попробуй позже")

if __name__ == "__main__":
    logging.info("Бот запущен")
    bot.infinity_polling(skip_pending=True, timeout=20, long_polling_timeout=20)