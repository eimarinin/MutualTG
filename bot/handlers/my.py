# bot/handlers/my.py
def register_my_handler(bot, sheets):
    @bot.message_handler(commands=['my'])
    def my_channels(message):
        user_id = message.from_user.id
        records = sheets.sheet.findall(str(user_id), in_column=2)

        if not records:
            bot.reply_to(message, "У тебя пока нет каналов в базе\n\nДобавь первый через /add")
            return

        channels = []
        for rec in records:
            row = rec.row
            data = sheets.sheet.row_values(row)
            link = data[3] if len(data) > 3 else "???"
            status = data[4] if len(data) > 4 else "в очереди"
            channels.append(f"• {link} — {status}")

        count = len(channels)
        text = f"Твои каналы в базе ({count}):\n\n" + "\n".join(channels) + \
               f"\n\nДобавить ещё → /add\nУдалить один → /delete"

        bot.reply_to(message, text, disable_web_page_preview=True)