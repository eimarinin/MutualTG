# config.py
import os
from dataclasses import dataclass
from dotenv import load_dotenv

# Загружаем .env только локально (на Render его нет — и это нормально)
if os.path.exists(".env"):
    load_dotenv()

@dataclass(frozen=True)
class Config:
    BOT_TOKEN: str = os.getenv("BOT_TOKEN")
    SHEET_ID: str = os.getenv("SHEET_ID")
    SHEET_NAME: str = os.getenv("SHEET_NAME", "Лист1")

    def __post_init__(self):
        # Проверка, что переменные точно заданы (на Render упадёт сразу, если забыли)
        if not self.BOT_TOKEN or not self.SHEET_ID:
            raise ValueError("BOT_TOKEN и SHEET_ID обязательны в env!")

config = Config()