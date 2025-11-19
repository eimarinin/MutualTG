# bot/utils/validators.py
import telebot.async_telebot

async def validate_and_check_channel(bot, link: str) -> tuple[bool, str]:
    try:
        username = link[1:] if link.startswith("@") else link.split("t.me/")[1]
        chat = await bot.get_chat(username)

        if chat.type not in ["channel", "supergroup"]:
            return False, "Это не канал и не публичная группа"

        if chat.type == "channel" and not chat.username:
            return False, "Приватные каналы без @username не принимаем"

        return True, ""

    except telebot.async_telebot.ApiTelegramException as e:
        if "chat not found" in str(e):
            return False, "Канал не найден — возможно, он удалён или ссылка неверная"
        if "blocked" in str(e):
            return False, "Бот заблокирован в этом канале"
        return False, "Не удалось проверить канал"
    except:
        return False, "Ошибка проверки. Попробуй позже"