from config import load_config


class TelegramService:

    def __init__(self):

        config = load_config()

        self.token = config.get("telegram", {}).get("token")
        self.chat_id = config.get("telegram", {}).get("chat_id")

    def enabled(self):

        return bool(self.token and self.chat_id)

    def send(self, message):

        if not self.enabled():
            print("Telegram no configurado.")
            return

        print("Enviando mensaje a Telegram...")