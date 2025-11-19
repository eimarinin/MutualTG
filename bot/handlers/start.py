# bot/handlers/start.py
from telebot.types import ReplyKeyboardRemove

def register_start_handler(bot):
    @bot.message_handler(commands=['start'])
    @bot.message_handler(content_types=['start'])
    def start(message):
        text = (
            "Привет! Добро пожаловать в @MutualTG — честные взаимные подписки\n\n"
            "Мы только начали, но уже собираем живую и адекватную базу\n"
            "Никаких ботов, накрутки и спама — только реальный рост вместе\n\n"
            "Что можно сделать:\n"
            "• /add — добавить свой канал\n"
            "• /my — посмотреть свой канал и статус\n"
            "• /delete — удалить свой канал из базы\n"
            "• /rules — правила сообщества\n"
            "• /channel — наш канал с новостями\n\n"
            "Готов расти честно? Жми /add и кидай ссылку"
        )
        bot.send_message(message.chat.id, text, reply_markup=ReplyKeyboardRemove())