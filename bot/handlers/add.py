# bot/handlers/add.py
import re
import asyncio
from bot.utils.validators import validate_and_check_channel

def register_add_handler(bot, sheets):
    # Состояния пользователей: кто сейчас добавляет канал
    user_states = {}  # {user_id: "waiting_for_link"}

    # Команда /add — начинаем процесс добавления
    @bot.message_handler(commands=['add'])
    def add_start(message):
        user_states[message.from_user.id] = "waiting_for_link"
        bot.reply_to(message,
                     "Отлично! Пришли ссылку на свой канал:\n"
                     "Например: t.me/mychannel или @mychannel")

    # Ловим ТОЛЬКО сообщения от тех, кто в состоянии "waiting_for_link"
    @bot.message_handler(func=lambda m: m.from_user.id in user_states and user_states[m.from_user.id] == "waiting_for_link")
    def process_link(message):
        user_id = message.from_user.id
        raw_link = message.text.strip()

        # Очистка ссылки
        link = re.sub(r"^https?://", "", raw_link)
        link = re.sub(r"^telegram\.me/", "t.me/", link)
        link = re.sub(r"^t\.me/", "t.me/", link)
        link = link.split("?")[0].split("#")[0].rstrip("/")

        if not (link.startswith("t.me/") and len(link) > 5) and not (link.startswith("@") and len(link) > 1):
            bot.reply_to(message, "Неверный формат\n\nПримеры:\nt.me/mychannel\n@mychannel")
            return

        if sheets.is_already_added(user_id):
            bot.reply_to(message, "Ты уже добавил канал! Используй /my или /delete")
            del user_states[user_id]
            return

        # Проверка существования канала
        loop = asyncio.get_event_loop()
        exists, error_msg = loop.run_until_complete(validate_and_check_channel(bot, link))
        if not exists:
            bot.reply_to(message, f"Не удалось добавить:\n\n{error_msg}")
            return

        # Сохраняем
        if sheets.add_channel(user_id,
                             f"@{message.from_user.username}" if message.from_user.username else "без_юзернейма",
                             link):
            bot.reply_to(message,
                "Готово! Твой канал добавлен и проверен\n\n"
                "Как только найду взаимку — напишу в личку\n"
                "Спасибо, что с нами!")
        else:
            bot.reply_to(message, "Ошибка записи. Попробуй позже")

        # Сбрасываем состояние
        del user_states[user_id]