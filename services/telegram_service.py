import os

from telegram import Bot

from app_config import APP_NAME, APP_ICON


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
            text=message,
            link_preview_options={
                "is_disabled": True
            }
        )

    async def send_house(self, house):

        message = (
            f"{APP_ICON} {APP_NAME}\n\n"
            f"🏠 {house.title}\n"
            f"💰 {house.price:.0f} €\n"
            f"📐 {house.size:.0f} m²\n"
            f"🔗 {house.url}"
        )

        await self.send(message)

    async def send_houses(self, search, houses):

        if not houses:
            return

        message = (
            f"{APP_ICON} {APP_NAME}\n\n"
            f"📍 Búsqueda: {search['name']}\n"
            f"🆕 Viviendas nuevas: {len(houses)}\n\n"
        )

        for house in houses:

            message += (
                f"• {house.title}\n"
                f"💰 {house.price:.0f} €\n"
                f"📐 {house.size:.0f} m²\n"
                f"🔗 {house.url}\n\n"
            )

        await self.send(message)