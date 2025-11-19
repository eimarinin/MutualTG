# bot/handlers/channel.py
def register_channel_handler(bot):
    @bot.message_handler(commands=['channel'])
    def channel(message):
        text = "Наш канал с новостями, отзывами и топами:\n\n@MutualTG\n\nТам видно, сколько нас и как всё работает"
        bot.send_message(message.chat.id, text)