"""
пример работы бота телеграмм

"""

import os
from dotenv import load_dotenv  # pip3 install python-dotenv
from telethon import TelegramClient, events  # pip3 install Telethon

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
print((dotenv_path))
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
app_api_id = os.getenv("TLG_APP_API_ID")
app_api_hash = os.getenv("TLG_APP_API_HASH")
app_name = os.getenv("TLG_APP_NAME")
bot_token = os.getenv("I_BOT_TOKEN")

"""
print(app_api_hash)
print(app_api_id)
print(app_name)
print(bot_token)
"""


bot = TelegramClient(app_name, app_api_id, app_api_hash).start(bot_token=bot_token)
client = [] # клиент

@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    """Send a message when the command /start is issued."""
    await event.respond('Hi!')
    raise events.StopPropagation

@bot.on(events.NewMessage)
async def echo(event):
    """Echo the user message."""
    chat = await event.get_input_chat()
    sender = await event.get_sender()
    buttons = await event.get_buttons()
    print(sender.id)
    await event.respond(event.text)

def main():
    """Start the bot."""
    bot.run_until_disconnected()

if __name__ == '__main__':
    main()