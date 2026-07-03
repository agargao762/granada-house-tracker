import os

from telegram import Bot

from app_config import APP_NAME, APP_ICON


class TelegramService:

    def __init__(self):
        self.token = os.getenv("TELEGRAM_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")

    def enabled(self):
        return bool(self.token and self.chat_id)
    
    def format_house(self, house):

        return (
            f"🏠 {house.title}\n"
            f"💰 {house.price:.0f} €\n"
            f"📐 {house.size:.0f} m²\n"
            f"🛏 {house.bedrooms} hab | 🚿 {house.bathrooms} baños\n"
            f"🔗 {house.url}"
        )

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
            f"{self.format_house(house)}"
        )

        await self.send(message)

    async def send_houses(self, search, new_houses, updated_houses):

        if not new_houses and not updated_houses:
            return

        lines = [
            f"{APP_ICON} {APP_NAME}",
            "",
            f"📍 {search['name']}",
            "",
            f"🆕 Viviendas nuevas: {len(new_houses)}",
            "",
        ]

        for house in new_houses:

            lines.append(self.format_house(house))
            lines.append("")
            lines.append("━━━━━━━━━━━━━━━━━━")
            lines.append("")

        if updated_houses:

            lines.append("💰 Cambios de precio")
            lines.append("")

            for house, old_price in updated_houses:

                lines.append(f"🏠 {house.title}")
                lines.append(f"⬇️ {old_price:.0f} € → {house.price:.0f} €")
                lines.append(f"🔗 {house.url}")
                lines.append("")
                lines.append("━━━━━━━━━━━━━━━━━━")
                lines.append("")

        await self.send("\n".join(lines))