# bot/handlers/delete.py
def register_delete_handler(bot, sheets):
    @bot.message_handler(commands=['delete'])
    def delete_channel(message):
        user_id = message.from_user.id
        records = sheets.sheet.findall(str(user_id), in_column=2)

        if not records:
            bot.reply_to(message, "У тебя нет канала в базе\n\nДобавь через /add")
            return

        row = records[0].row
        sheets.sheet.delete_rows(row)

        # Обновляем кэш
        sheets.all_ids.discard(str(user_id))

        bot.reply_to(message, "Твой канал удалён из базы\n\nЕсли передумал — просто жми /add")