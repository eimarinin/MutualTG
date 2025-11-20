# bot/handlers/add.py
import re
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.utils.validators import validate_and_check_channel

def register_add_handler(bot, sheets):
    user_states = {}

    @bot.message_handler(commands=['add'])
    def add_start(message):
        user_id = message.from_user.id
        user_states[user_id] = "waiting_for_link"

        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("Отмена", callback_data="cancel_add"))

        bot.reply_to(message,
                     "Пришли ссылку на свой канал:\n"
                     "Например: @mychannel или t.me/mychannel\n\n"
                     "Можешь добавить сколько угодно каналов — просто повторяй /add",
                     reply_markup=markup)
        
    # Кнопка "Отмена"
    @bot.callback_query_handler(func=lambda call: call.data == "cancel_add")
    def cancel_add(call):
        user_id = call.from_user.id
        if user_id in user_states:
            del user_states[user_id]
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="Добавление канала отменено"
        )

    @bot.message_handler(func=lambda m: m.from_user.id in user_states and user_states[m.from_user.id] == "waiting_for_link")
    def process_link(message):
        user_id = message.from_user.id
        raw_link = message.text.strip()

        # Если прислал команду — выходим
        if raw_link.startswith("/"):
            if user_id in user_states:
                del user_states[user_id]
            bot.reply_to(message, "Добавление отменено")
            return
        
        # === ОЧИСТКА ССЫЛКИ ===
        link = re.sub(r"https?://", "", raw_link, flags=re.IGNORECASE)
        link = re.sub(r"telegram\.me/", "t.me/", link, flags=re.IGNORECASE)
        link = re.sub(r"t\.me/", "t.me/", link, flags=re.IGNORECASE)
        link = link.split("?")[0].split("#")[0].rstrip("/").strip()


        # Валидация формата
        if not (link.startswith("t.me/") and len(link) > 5) and not (link.startswith("@") and len(link) > 1):
            bot.reply_to(message, "Неверный формат\n\nПримеры:\n• t.me/mychannel\n• @mychannel")
            return

        # Проверяем дубли
        exists, result = validate_and_check_channel(bot, link, user_id)
        if not exists:
            bot.reply_to(message, f"Не удалось добавить канал:\n\n{result}")
            return

        # Проверка канала
        if sheets.is_channel_already_added(user_id, result):
            bot.reply_to(message, f"Канал {result} уже есть у тебя в базе!\n\nПосмотреть все → /my")
            del user_states[user_id]
            return

        # Сохраняем
        success = sheets.add_channel(
            user_id,
            f"@{message.from_user.username}" if message.from_user.username else "без_юзернейма",
            result
        )

        if success:
            count = sheets.get_user_channels_count(user_id)
            bot.reply_to(message,
                f"Готово! Канал {result} успешно добавлен\n\n"
                f"У тебя в базе: {count} канал(ов)\n"
                "Как только найду взаимку — сразу напишу в личку\n"
                "Спасибо, что с нами!")
        else:
            bot.reply_to(message, "Ошибка записи в базу. Попробуй позже")

        del user_states[user_id]