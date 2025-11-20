# bot/handlers/__init__.py
from .start import register_start_handler
from .add import register_add_handler
from .my import register_my_handler
from .delete import register_delete_handler
from .rules import register_rules_handler
from .channel import register_channel_handler

def register_handlers(bot, sheets):
    register_start_handler(bot)
    register_add_handler(bot, sheets)
    register_my_handler(bot, sheets)
    register_delete_handler(bot, sheets)
    register_rules_handler(bot)
    register_channel_handler(bot)

    # Ловим любой текст, который не попал под команды и не в состоянии добавления
    @bot.message_handler(func=lambda message: True)
    def unknown_message(message):
        user_id = message.from_user.id
        # Если он сейчас добавляет канал — не трогаем (это ловит add.py)
        if hasattr(bot, 'user_states') and user_id in bot.user_states:
            return

        bot.reply_to(message,
                     "Не понял, что ты написал\n\n"
                     "Доступные команды:\n"
                     "/start — приветствие\n"
                     "/add — добавить канал\n"
                     "/my — мои каналы\n"
                     "/delete — удалить канал\n"
                     "/rules — правила\n"
                     "/channel — наш канал")