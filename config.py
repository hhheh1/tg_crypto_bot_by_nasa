import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
DATABASE_PATH = os.getenv("DATABASE_PATH", "bot.db")
BINANCE_API_URL = os.getenv("BINANCE_API_URL", "https://api.binance.com")
