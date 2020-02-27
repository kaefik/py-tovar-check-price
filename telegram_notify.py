"""
    отправка нотификации клиенту используя телеграмм бота

    использовать будем https://github.com/LonamiWebs/Telethon
"""

import os
from dotenv import load_dotenv
from telethon import TelegramClient, events, sync

class SendNotify:

    # инициализация
    def __init__(self):
        dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
        # print((dotenv_path))
        if os.path.exists(dotenv_path):
            load_dotenv(dotenv_path)
        self.app_api_id = os.getenv("TLG_APP_API_ID")
        self.app_api_hash = os.getenv("TLG_APP_API_HASH")
        self.app_name = os.getenv("TLG_APP_NAME")
        self.bot_token = os.getenv("I_BOT_TOKEN")
        self.client = os.getenv("TLG_CLIENT")

        self._tlg = TelegramClient(self.app_name , self.app_api_id, self.app_api_hash)
        self._tlg.start(bot_token=self.bot_token)

    # добавление клиента которому нужно отправлять нотификации
    def add_clent(self, event):
        pass

    # отправка всем клиентам сообщения msg
    def send_msg(self, msg):
        self._tlg.send_message(self.client, msg)

if __name__ == "__main__":
    tlg = SendNotify()
    print(tlg.send_msg("привет!"))

