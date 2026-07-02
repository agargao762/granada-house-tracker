import os

from telegram import Bot


class TelegramService:

    def __init__(self):
        self.token = os.getenv("TELEGRAM_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")

    def enabled(self):
        return bool(self.token and self.chat_id)

    async def send(self, message):

        if not self.enabled():
            print("Telegram no configurado.")
            return

        bot = Bot(token=self.token)

        await bot.send_message(
            chat_id=self.chat_id,
            text=message
        )