# bot/__init__.py
from .handlers.start import register_start_handler
from .handlers.add import register_add_handler
from .handlers.my import register_my_handler
from .handlers.delete import register_delete_handler
from .handlers.rules import register_rules_handler
from .handlers.channel import register_channel_handler

def register_handlers(bot, sheets):
    register_start_handler(bot)
    register_add_handler(bot, sheets)
    register_my_handler(bot, sheets)
    register_delete_handler(bot, sheets)
    register_rules_handler(bot)
    register_channel_handler(bot)