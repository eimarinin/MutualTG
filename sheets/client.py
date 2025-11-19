# sheets/client.py
import gspread
from google.oauth2.service_account import Credentials
from config import config
from datetime import datetime
import logging

"""
Google Sheets клиент для mutual-бота
Использует сервисный аккаунт + Sheets API
"""

class SheetsClient:
    def __init__(self):
        scopes = ["https://www.googleapis.com/auth/spreadsheets"]
        creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
        self.client = gspread.authorize(creds)
        self.sheet = self.client.open_by_key(config.SHEET_ID).worksheet(config.SHEET_NAME)
        self.all_ids = set(self.sheet.col_values(2)[1:])  # колонка B — user_id (строка)

    def is_already_added(self, user_id: int) -> bool:
        return str(user_id) in self.all_ids

    def add_channel(self, user_id: int, username: str, channel_link: str) -> bool:
        try:
            self.sheet.append_row([
                datetime.now().strftime("%Y-%m-%d %H:%M"),
                user_id,
                username,
                channel_link,
                "в очереди"
            ])
            self.all_ids.add(str(user_id))  # обновляем кэш
            return True
        except Exception as e:
            logging.error(f"Sheets error: {e}")
            return False