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

    # sheets/client.py
    def is_channel_already_added(self, user_id: int, channel_link: str) -> bool:
        """
        Проверяет, добавлял ли конкретный пользователь уже конкретный канал
        """
        try:
            # Приводим ссылку к единому виду: @username в нижнем регистре
            normalized = channel_link.lower().lstrip("@")
            if "t.me/" in normalized:
                normalized = normalized.split("t.me/")[1]

            # Ищем все строки пользователя
            records = self.sheet.findall(str(user_id), in_column=2)  # колонка B — user_id
            for record in records:
                row_data = self.sheet.row_values(record.row)
                if len(row_data) > 3:
                    existing_link = row_data[3].lower().lstrip("@")
                    if "t.me/" in existing_link:
                        existing_link = existing_link.split("t.me/")[1]
                    if existing_link == normalized:
                        return True
            return False
        except:
            return False

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
    
    def get_user_channels_count(self, user_id: int) -> int:
        """Сколько каналов у пользователя в базе"""
        try:
            records = self.sheet.findall(str(user_id), in_column=2)  # колонка B — user_id
            return len(records)
        except:
            return 0