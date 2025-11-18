# sheets/client.py
import gspread
from google.oauth2.service_account import Credentials
from config import Config
from datetime import datetime
import logging

# YARD-style doc
"""
Google Sheets клиент для mutual-бота
Использует сервисный аккаунт + Sheets API
"""

class SheetsClient:
    def __init__(self):
        scopes = ["https://www.googleapis.com/auth/spreadsheets"]
        creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
        self.client = gspread.authorize(creds)
        self.sheet = self.client.open_by_key(Config.SHEET_ID).worksheet(Config.SHEET_NAME)

    def add_channel(self, user_id: int, username: str, channel_link: str) -> bool:
        """
        Добавляет канал в базу
        Returns: True если успешно
        """
        try:
            self.sheet.append_row([
                datetime.now().strftime("%Y-%m-%d %H:%M"),
                user_id,
                username,
                channel_link,
                "в очереди"
            ])
            return True
        except Exception as e:
            logging.error(f"Sheets error: {e}")
            return False