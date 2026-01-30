import sqlite3 as sq


def init_database(db_path):
    with sq.connect(db_path) as conn:
        cur = conn.cursor()

        cur.execute(
            """CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    telegram_id INTEGER UNIQUE,
                    username TEXT,
                    created_at DATETIME
                    )"""
        )

        cur.execute(
            """CREATE TABLE IF NOT EXISTS supported_coins (
                    id INTEGER PRIMARY KEY,
                    ticker TEXT UNIQUE,
                    name TEXT
                    )"""
        )


def register_user(db_path, telegram_id, username, created_at):
    with sq.connect(db_path) as conn:
        cur = conn.cursor()

        cur.execute(
            """INSERT OR IGNORE INTO users (telegram_id, username, created_at) VALUES (?, ?, ?)""",
            (telegram_id, username, created_at),
        )


def get_user(telegram_id):
    pass


def get_supported_coins():
    pass


def is_coin_supported(ticker):
    pass
