import sqlite3 as sq
import requests
import re

from config import DATABASE_PATH, BINANCE_API_URL


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
    # только A-Z/0-9
    VALID_TICKER_RE = re.compile(r"^[A-Z0-9]{2,15}$")

    # фиатные коды
    FIAT_CODES = (
        "USD",
        "EUR",
        "GBP",
        "TRY",
        "RUB",
        "UAH",
        "JPY",
        "CNY",
        "AUD",
        "CAD",
        "CHF",
        "BRL",
        "INR",
        "ZAR",
    )

    # точные стейблы
    STABLES_EXACT = {
        "USDT",
        "USDC",
        "FDUSD",
        "BUSD",
        "TUSD",
        "DAI",
        "USDP",
        "PAX",
        "UST",
        "USTC",
        "EURC",
        "EURT",
    }

    # мощный фильтр: убираем тикеры с любым фиат-кодом внутри (RLUSD, XUSD, USDE...)
    FIAT_LIKE_RE = re.compile(r"(" + "|".join(FIAT_CODES) + r")")

    # --- exchangeInfo -> все активные пары к USDT ---
    exchange_info = requests.get(f"{BINANCE_API_URL}/api/v3/exchangeInfo").json()
    usdt_symbols = {
        s["symbol"]
        for s in exchange_info["symbols"]
        if s.get("quoteAsset") == "USDT" and s.get("status") == "TRADING"
    }

    # --- ticker 24hr -> сортировка по объёму ---
    tickers = requests.get(f"{BINANCE_API_URL}/api/v3/ticker/24hr").json()
    filtered = [t for t in tickers if t.get("symbol") in usdt_symbols]
    filtered.sort(key=lambda x: float(x.get("quoteVolume", 0) or 0), reverse=True)

    # --- собираем ВСЕ тикеры (без ограничения top-50) ---
    coins = []
    seen = set()

    for t in filtered:
        sym = t.get("symbol", "")
        if not sym.endswith("USDT"):
            continue

        base = sym[:-4]

        # 1) мусорные тикеры (币安人生 и т.п.)
        if not VALID_TICKER_RE.fullmatch(base):
            continue

        # 2) точные стейблы
        if base in STABLES_EXACT:
            continue

        # 3) любые тикеры с фиат-кодами внутри (RLUSD, USD1, EURX...)
        if FIAT_LIKE_RE.search(base):
            continue

        if base not in seen:
            seen.add(base)
            coins.append(base)

    # --- запись всех тикеров в sqlite ---
    with sq.connect(db_path) as conn:
        cur = conn.cursor()
        cur.executemany(
            "INSERT OR IGNORE INTO supported_coins (ticker) VALUES (?)",
            [(c,) for c in coins],
        )


def get_supported_coins(db_path):
    with sq.connect(db_path) as conn:
        cur = conn.cursor()

        cur.execute("""SELECT ticker FROM supported_coins""")

        rows = cur.fetchall()

        return [row[0] for row in rows]


def is_coin_supported(ticker):
    return ticker in get_supported_coins(DATABASE_PATH)
