import json
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env")

DATABASE_PATH = BASE_DIR / "data" / "houses.db"

CONFIG_FILE = BASE_DIR / "config.json"


def load_config():
    with open(CONFIG_FILE, encoding="utf-8") as f:
        return json.load(f)