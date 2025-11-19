# main.py
import telebot
from telebot.types import ReplyKeyboardRemove
from config import config
from sheets.client import SheetsClient
import logging
import re

logging.basicConfig(level=logging.INFO)

bot = telebot.TeleBot(config.BOT_TOKEN)
sheets = SheetsClient()

@bot.message_handler(commands=['start'])
@bot.message_handler(content_types=['start'])
def start(message):
    text = (
        "Привет! Я бот взаимных подписок @MutualTG\n\n"
        "Мы только-только запустились — сейчас в базе меньше 20 каналов, зато все живые и по-честному\n"
        "Давай расти вместе без накрутки и ботов\n\n"
        "Просто пришли мне ссылку на свой канал:\n"
        "→ t.me/твойканал\n"
        "→ или @твойканал\n\n"
        "Я сохраню и как только найду подходящий — сразу напишу тебе в личку с предложением взаимной подписки\n\n"
        "Требования простые:\n"
        "• ~25 живых подписчиков\n"
        "• без 18+, политики, крипты, казино\n"
        "• подписка взаимная и не удаляется\n\n"
        "Готов? Кидай ссылку — начнём прямо сейчас"
    )
    bot.send_message(message.chat.id, text, disable_web_page_preview=True)


@bot.message_handler(func=lambda m: True)
def save_channel(message):
    raw_link = message.text.strip()
    user_id = message.from_user.id
    username = f"@{message.from_user.username}" if message.from_user.username else "без_юзернейма"

    # Супер-надёжная очистка и валидация ссылки
    link = re.sub(r"^https?://", "", raw_link)
    link = re.sub(r"^telegram\.me/", "t.me/", link)
    link = re.sub(r"^t\.me/", "t.me/", link)
    link = link.split("?")[0].split("#")[0].rstrip("/")

    if not (link.startswith("t.me/") and len(link) > 5) and not (link.startswith("@") and len(link) > 1):
        bot.reply_to(message, "Пожалуйста, пришли нормальную ссылку на канал:\n"
                             "Примеры:\nt.me/MutualTG\n@MutualTG")
        return

    # Защита от дублей
    if sheets.is_already_added(user_id):
        bot.reply_to(message, "Ты уже в базе! Как только найду тебе взаимку — сразу напишу в личку")
        return

    # Сохраняем
    success = sheets.add_channel(user_id, username, link)
    if success:
        bot.reply_to(message, 
            "Супер! Твой канал добавлен\n\n"
            "Как только появится подходящий канал — я лично напишу тебе в ЛС\n"
            "Можешь позвать друзей — чем нас больше, тем быстрее взаимки")
    else:
        bot.reply_to(message, "Что-то пошло не так, попробуй ещё раз через минуту")


if __name__ == "__main__":
    logging.info("Бот запущен")
    bot.infinity_polling(skip_pending=True, timeout=20, long_polling_timeout=20)