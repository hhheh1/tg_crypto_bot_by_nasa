import telebot
from datetime import datetime
import requests

from config import TELEGRAM_BOT_TOKEN, DATABASE_PATH, BINANCE_API_URL
import database as db


bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)


@bot.message_handler(commands=["start"])
def handle_start(message):
    telegram_id = message.from_user.id
    username = message.from_user.username
    created_at = datetime.fromtimestamp(message.date).isoformat()

    user = db.get_user(DATABASE_PATH, telegram_id)
    if user is None:
        db.register_user(DATABASE_PATH, telegram_id, username, created_at)
        bot.send_message(
            message.chat.id,
            f"{message.from_user.first_name}, поздравляю с успешной регистрацией в мессенджере MAX!",
        )

    bot.send_message(
        message.chat.id,
        """Привет, малыш!\nОзнакомься с командами, пожалуйста!\n
/price {ticker} - Получает текущую цену из Binance API.\n
/stats {ticker} - Получает статистику за 24 часа из Binance API.\n
/profile - Выводит профиль пользователя и список поддерживаемых валют.\n\n"""
        + "Поддерживаемые валюты:\n"
        + " ".join(db.coins),
    )


@bot.message_handler(commands=["price"])
def handle_price(message):
    pass


@bot.message_handler(commands=["stats"])
def handle_stats(message):
    pass


@bot.message_handler(commands=["profile"])
def handle_profile(message):
    pass


if __name__ == "__main__":
    db.init_database(DATABASE_PATH)
    db.register_supported_coins(DATABASE_PATH)
    print("BOT STARTED")
    bot.polling(non_stop=True)
