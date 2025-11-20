# bot/handlers/delete.py
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def register_delete_handler(bot, sheets):
    @bot.message_handler(commands=['delete'])
    def delete_start(message):
        user_id = message.from_user.id
        records = sheets.sheet.findall(str(user_id), in_column=2)

        if not records:
            bot.reply_to(message, "У тебя нет каналов в базе\n\nДобавь через /add")
            return

        markup = InlineKeyboardMarkup(row_width=1)
        for rec in records:
            row_data = sheets.sheet.row_values(rec.row)
            link = row_data[3] if len(row_data) > 3 else "???"
            row_id = rec.row
            markup.add(InlineKeyboardButton(
                text=f"Удалить {link}",
                callback_data=f"delete_channel_{row_id}"
            ))

        markup.add(InlineKeyboardButton("Отмена", callback_data="delete_cancel"))
        bot.send_message(message.chat.id, "Выбери канал для удаления:", reply_markup=markup)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("delete_channel_"))
    def confirm_delete(call):
        row_id = int(call.data.split("_")[-1])
        row_data = sheets.sheet.row_values(row_id)
        link = row_data[3] if len(row_data) > 3 else "???"

        # Удаляем строку
        sheets.sheet.delete_rows(row_id)

        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=f"Канал {link} удалён из базы"
        )
        bot.answer_callback_query(call.id)

    @bot.callback_query_handler(func=lambda call: call.data == "delete_cancel")
    def cancel_delete(call):
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="Удаление отменено"
        )
        bot.answer_callback_query(call.id)