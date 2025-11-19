# bot/handlers/my.py
def register_my_handler(bot, sheets):
    @bot.message_handler(commands=['my'])
    def my_channel(message):
        user_id = message.from_user.id
        records = sheets.sheet.findall(str(user_id), in_column=2)  # ищем в колонке B

        if not records:
            bot.reply_to(message, "Ты ещё не добавлял канал\n\nЖми /add и пришли ссылку")
            return

        row = records[0].row
        data = sheets.sheet.row_values(row)
        link = data[3]
        status = data[4] if len(data) > 4 else "в очереди"

        text = f"Твой канал в базе:\n\n{link}\n\nСтатус: {status}\n\nЯ ищу тебе взаимки"
        bot.reply_to(message, text)