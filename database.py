import sqlite3 as sq
import requests
import re

from config import BINANCE_API_URL


coins = [
    "BTC",
    "ETH",
    "BNB",
    "SOL",
    "XRP",
    "ADA",
    "DOGE",
    "DOT",
    "AVAX",
    "LINK",
    "MATIC",
    "ATOM",
    "LTC",
    "BCH",
    "ETC",
    "XLM",
    "TRX",
    "FIL",
    "NEAR",
    "ICP",
    "APT",
    "ARB",
    "OP",
    "SUI",
    "INJ",
    "AAVE",
    "UNI",
    "MKR",
    "SNX",
    "CRV",
    "SUSHI",
    "RUNE",
    "EGLD",
    "ALGO",
    "GRT",
    "FLOW",
    "QNT",
    "DYDX",
    "IMX",
    "FET",
    "RNDR",
    "PEPE",
    "FLOKI",
    "BONK",
    "WIF",
    "TIA",
    "JUP",
    "PYTH",
    "SEI",
    "TAO",
    "ZK",
    "ZRO",
    "TON",
]


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
                    ticker TEXT UNIQUE
                    )"""
        )


def register_user(db_path, telegram_id, username, created_at):
    with sq.connect(db_path) as conn:
        cur = conn.cursor()

        cur.execute(
            """INSERT INTO users (telegram_id, username, created_at) VALUES (?, ?, ?)""",
            (telegram_id, username, created_at),
        )


def get_user(db_path, telegram_id):
    with sq.connect(db_path) as conn:
        cur = conn.cursor()

        cur.execute(
            """SELECT id, telegram_id, username, created_at FROM users WHERE telegram_id = ?""",
            (telegram_id,),
        )

    return cur.fetchone()


def register_supported_coins(db_path):
    with sq.connect(db_path) as conn:
        cur = conn.cursor()
        cur.executemany(
            "INSERT OR IGNORE INTO supported_coins (ticker) VALUES (?)",
            [(t,) for t in coins],
        )


def get_supported_coins():
    pass


def is_coin_supported(ticker):
    pass
