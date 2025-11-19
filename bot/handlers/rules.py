# bot/handlers/rules.py
def register_rules_handler(bot):
    @bot.message_handler(commands=['rules'])
    def rules(message):
        text = (
            "Правила @MutualTG — просто и по-человечески:\n\n"
            "Разрешено:\n"
            "• Живые каналы от ~25 подписчиков\n"
            "• Любая тематика, кроме запрещённой\n\n"
            "Запрещено:\n"
            "• 18+, политика, казино, крипто-скам\n"
            "• Накрутка, боты, спам\n"
            "• Удаление обратной подписки\n\n"
            "Нарушил — бан навсегда\n"
            "Качество важнее количества"
        )
        bot.reply_to(message, text)