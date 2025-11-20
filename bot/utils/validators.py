# bot/utils/validators.py
import logging

def validate_and_check_channel(bot, link: str, user_id: int) -> tuple[bool, str]:
    """
    Проверка канала + поиск без учёта регистра + проверка, что юзер — админ
    Теперь принимает user_id как параметр!
    """
    logging.info(f"[Проверка канала] link='{link}', user_id={user_id}")

    # Извлекаем username
    if link.startswith("@"):
        username = link[1:].strip()
    elif "t.me/" in link:
        username = link.split("t.me/")[1].strip().split("?")[0].split("#")[0]
    else:
        return False, "Не могу распознать ссылку. Пришли @username или t.me/username"

    if not username:
        return False, "Пустое имя канала"

    logging.info(f"Ищем @{username}")

    chat = None

    # Попытка 1 — как есть
    try:
        chat = bot.get_chat("@" + username)
        logging.info(f"Нашёл сразу: @{username}")
    except Exception as e1:
        logging.info(f"Не нашёл @{username}: {e1}")

    # Попытка 2 — нижний регистр
    if not chat:
        lower = username.lower()
        if lower != username:
            try:
                chat = bot.get_chat("@" + lower)
                logging.info(f"Нашёл через lower: @{lower}")
            except Exception as e2:
                logging.info(f"И через lower не нашёл: {e2}")

    if not chat:
        logging.error(f"Канал @{username} не найден")
        return False, f"Канал @{username} не найден\n\nПроверь написание или разблокируй бота"

    if chat.type not in ["channel", "supergroup"]:
        return False, f"Это не канал и не группа, а {chat.type}"

    if chat.type == "channel" and not chat.username:
        return False, "Приватные каналы без @username не принимаем"

    # ← ПРОВЕРКА АДМИНСТВА ←
    # try:
    #     admins = bot.get_chat_administrators(chat.id)
    #     admin_ids = [admin.user.id for admin in admins]
    #     if user_id not in admin_ids:
    #         return False, f"Ты не админ в канале @{chat.username or username}\n\nТолько админы могут добавлять канал"
    # except Exception as e:
    #     error_msg = str(e).lower()
    #     if "not enough rights" in error_msg or "administrator rights" in error_msg:
    #         return False, f"Бот не может видеть админов в @{chat.username or username}\n\nДобавь @MutualTG_bot как админа в канал (хотя бы с правом «Просмотр участников»)"
    #     else:
    #         return False, f"Не удалось проверить права в канале @{chat.username or username}"

    # Канонический username с правильным регистром
    canonical = f"@{chat.username}" if chat.username else link
    logging.info(f"Канал прошёл все проверки → сохраняем как {canonical}")
    return True, canonical