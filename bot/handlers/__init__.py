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