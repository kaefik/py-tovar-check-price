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
        print((dotenv_path))
        if os.path.exists(dotenv_path):
            load_dotenv(dotenv_path)
        self.api_id = os.getenv("TLG_API_ID")
        self.api_hash = os.getenv("TLG_API_HASH")
        client = TelegramClient('send_notify-kaefik', self.api_id, self.api_hash)
        client.start()
        """

        print(client.get_me().stringify())

        client.send_message('username', 'Hello! Talking to you from Telethon')
        client.send_file('username', '/home/myself/Pictures/holidays.jpg')

        client.download_profile_photo('me')
        messages = client.get_messages('username')
        messages[0].download_media()

        @client.on(events.NewMessage(pattern='(?i)hi|hello'))
        async def handler(event):
            await event.respond('Hey!')
        """

    # добавление клиента которому нужно отправлять нотификации
    def add_clent(self):
        pass

    # отправка всем клиентам сообщения msg
    def send_msg(self, msg):
        pass


if __name__ == "__main__":

    tlg = SendNotify()
    print(tlg.api_id)
