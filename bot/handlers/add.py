# bot/handlers/add.py
import re
import asyncio
from bot.utils.validators import validate_and_check_channel

def register_add_handler(bot, sheets):
    @bot.message_handler(commands=['add'])
    @bot.message_handler(func=lambda m: True)  # ловим любой текст как попытку добавить
    def add_channel(message):
        raw_link = message.text.strip()

        # Очистка ссылки
        link = re.sub(r"^https?://", "", raw_link)
        link = re.sub(r"^telegram\.me/", "t.me/", link)
        link = re.sub(r"^t\.me/", "t.me/", link)
        link = link.split("?")[0].split("#")[0].rstrip("/")

        if not (link.startswith("t.me/") and len(link) > 5) and not (link.startswith("@") and len(link) > 1):
            bot.reply_to(message, "Неверный формат ссылки\n\nПримеры:\nt.me/mychannel\n@mychannel")
            return

        user_id = message.from_user.id
        username = f"@{message.from_user.username}" if message.from_user.username else "без_юзернейма"

        # Проверка на дубликат
        if sheets.is_already_added(user_id):
            bot.reply_to(message, "Ты уже добавил канал! Используй /my, чтобы посмотреть, или /delete, чтобы удалить")
            return

        # Проверка существования канала
        loop = asyncio.get_event_loop()
        exists, error_msg = loop.run_until_complete(validate_and_check_channel(bot, link))

        if not exists:
            bot.reply_to(message, f"Не удалось добавить канал:\n\n{error_msg}\n\nПопробуй другую ссылку")
            return

        # Сохраняем
        if sheets.add_channel(user_id, username, link):
            bot.reply_to(message,
                "Готово! Твой канал успешно добавлен и проверен\n\n"
                "Как только найду подходящую взаимку — сразу напишу в личку\n"
                "Спасибо, что с нами — вместе растём честно")
        else:
            bot.reply_to(message, "Ошибка записи. Попробуй позже")