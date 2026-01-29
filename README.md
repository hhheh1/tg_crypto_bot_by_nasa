# 🪙 Crypto Price Tracker Bot

Учебный проект на **Python**, цель которого — научиться работать с:
- внешними API (`requests`) — Binance
- базой данных `SQLite` для хранения профилей пользователей и поддерживаемых валют
- raw SQL (без ORM)
- Telegram Bot API (`pyTelegramBotAPI`)
- переменными окружения (`python-dotenv`)

---

## 🎯 Цель проекта

Создать Telegram-бота, который позволяет:
- получать текущую цену криптовалюты
- получать статистику изменения за 24 часа
- просматривать профиль пользователя и список поддерживаемых валют

> Вся рыночная информация берётся из внешнего API Binance, данные в БД хранятся только по пользователям и поддерживаемым валютам.

---

## 📁 Рекомендуемая структура проекта

```
tg_crypto_bot/
├── main.py                # Главный файл с логикой бота
├── database.py            # Работа с базой данных (создание таблиц, SQL-запросы)
├── binance_api.py         # Функции для работы с API Binance
├── config.py              # Конфигурация (токен бота, путь к БД)
├── .env                   # Переменные окружения (токен бота)
├── .gitignore             # Игнорируемые файлы
├── requirements.txt       # Зависимости проекта
├── README.md              # Документация
└── bot.db                 # Файл базы данных SQLite (создаётся автоматически)
```

**Описание файлов:**

- `main.py` — основной файл с обработчиками команд (`/start`, `/price`, `/stats`, `/profile`)
- `database.py` — функции для работы с БД: создание таблиц, регистрация пользователей, получение данных
- `binance_api.py` — функции для запросов к Binance API (`get_price`, `get_stats`)
- `config.py` — настройки проекта (чтение токена из переменных окружения, путь к БД)
- `.env` — файл с токеном бота (не коммитится в git)
- `requirements.txt` — список зависимостей для установки через `pip install -r requirements.txt`

---

## ⚙️ Пример конфигурации (config.py)

Проект использует `python-dotenv` для загрузки переменных окружения из файла `.env`.

**Пример файла `config.py`:**

```python
import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
DATABASE_PATH = os.getenv("DATABASE_PATH", "bot.db")
BINANCE_API_URL = os.getenv("BINANCE_API_URL", "https://api.binance.com")
```

**Пример файла `.env`:**

```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
DATABASE_PATH=bot.db
BINANCE_API_URL=https://api.binance.com
```

**Использование в коде:**

```python
from config import TELEGRAM_BOT_TOKEN, DATABASE_PATH, BINANCE_API_URL

# Использование переменных
bot_token = TELEGRAM_BOT_TOKEN
db_path = DATABASE_PATH
binance_url = BINANCE_API_URL
```

---

## 🧱 Структура базы данных

### Таблица `users`

Хранит зарегистрированных пользователей Telegram.

| Поле | Тип | Описание |
|------|-----|----------|
| `id` | INTEGER PRIMARY KEY | Автоинкрементный ID записи |
| `telegram_id` | INTEGER UNIQUE | Уникальный ID пользователя в Telegram |
| `username` | TEXT | Имя пользователя (может быть NULL) |
| `created_at` | DATETIME | Дата и время регистрации |

---

### Таблица `supported_coins`

Список валют, которые бот поддерживает.

| Поле | Тип | Описание |
|------|-----|----------|
| `id` | INTEGER PRIMARY KEY | Автоинкрементный ID записи |
| `ticker` | TEXT UNIQUE | Тикер валюты (например, BTC, ETH) |
| `name` | TEXT | Полное название валюты |

---

## 🤖 Команды бота

### `/start`

Регистрирует пользователя в таблице `users`, если его ещё нет. Если пользователь уже зарегистрирован, ничего не делает.

**Пример ответа:**
```
Профиль создан ✅
```

---

### `/price {ticker}`

Получает текущую цену из Binance API.

- Использует публичный endpoint `/api/v3/ticker/price`
- Проверяет, что тикер есть в `supported_coins`
- Формирует символ для Binance как `{TICKER}USDT` (например, `BTCUSDT`)

**Пример запроса к API Binance:**
```
GET https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT
```

**Пример ответа от API:**
```json
{
  "symbol": "BTCUSDT",
  "price": "42350.12000000"
}
```

**Пример ответа бота:**
```
BTC
Цена: 42350 $
```

---

### `/stats {ticker}`

Получает статистику за 24 часа из Binance API.

- Использует публичный endpoint `/api/v3/ticker/24hr`
- Проверяет тикер в `supported_coins`
- Формирует символ для Binance как `{TICKER}USDT`

**Пример запроса к API Binance:**
```
GET https://api.binance.com/api/v3/ticker/24hr?symbol=BTCUSDT
```

**Пример ответа от API:**
```json
{
  "symbol": "BTCUSDT",
  "lastPrice": "42350.12",
  "highPrice": "42990.00",
  "lowPrice": "41800.00",
  "priceChangePercent": "2.1"
}
```

**Пример ответа бота:**
```
BTC — статистика за 24ч
Максимум: 42990 $
Минимум: 41800 $
Изменение: +2.1%
```

---

### `/profile`

Выводит профиль пользователя и список поддерживаемых валют.

**Пример ответа:**
```
Твой профиль:
ID: 123456789
Username: @nickname
Зарегистрирован: 2026-01-28

Поддерживаемые валюты:
BTC, ETH, SOL
```

---

## 🧠 SQL для проекта

Используется для:
- регистрации пользователя
- получения профиля
- получения списка поддерживаемых валют
- проверки существования тикера в `supported_coins`

**Типовые операции:**
- `INSERT` — добавление пользователя
- `SELECT` — получение данных
- `WHERE` — фильтрация
- `ORDER BY` — сортировка

Всё raw SQL, без ORM.

---

## 🔗 Полезные API Binance

| Endpoint | Что возвращает | Пример |
|----------|----------------|--------|
| `/api/v3/ticker/price` | Текущая цена криптовалюты | `https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT` |
| `/api/v3/ticker/24hr` | 24h статистика (high, low, изменение) | `https://api.binance.com/api/v3/ticker/24hr?symbol=BTCUSDT` |
| `/api/v3/exchangeInfo` | Список всех доступных торговых пар | `https://api.binance.com/api/v3/exchangeInfo` |

> **Примечание:** Для всех публичных API не нужен ключ.

---

## 🎯 Критерии приёмки

- ✅ Бот запускается и отвечает на все команды
- ✅ Пользователь успешно регистрируется через `/start`
- ✅ `/price` и `/stats` корректно получают данные из Binance
- ✅ `/profile` показывает информацию о пользователе и поддерживаемых валютах
- ✅ База данных не содержит лишних таблиц и записей
- ✅ Используются только raw SQL-запросы

---

## 📦 Зависимости

Для работы проекта потребуются следующие библиотеки:

```txt
pyTelegramBotAPI
requests
python-dotenv
```

Установка:
```bash
pip install pyTelegramBotAPI requests python-dotenv
```

Или через `requirements.txt`:
```bash
pip install -r requirements.txt
```

---

## 🔧 Настройка Git и GitHub

Перед началом работы нужно настроить Git и получить копию проекта.

### 1. Регистрация на GitHub

1. Перейдите на [github.com](https://github.com) и зарегистрируйте аккаунт (если его ещё нет)

### 2. Установка Git

**macOS:**
```bash
# Git обычно уже установлен, проверьте версию
git --version

# Если не установлен, установите через Homebrew
brew install git
```

**Windows:**
- Скачайте Git с [git-scm.com](https://git-scm.com/download/win)
- Установите с настройками по умолчанию
```

### 3. Настройка Git

Настройте имя и email (замените на свои данные):
```bash
git config --global user.name "Ваше Имя"
git config --global user.email "your.email@example.com"
```

### 4. Авторизация в Git

**Через HTTPS (простой способ):**
- При первом `git push` Git попросит ввести логин и пароль
- Для GitHub используйте Personal Access Token вместо пароля
- Создайте токен: GitHub → Settings → Developer settings → Personal access tokens → Generate new token
```

### 5. Форк репозитория

1. Откройте репозиторий: [https://github.com/chapppington/tg_crypto_bot](https://github.com/chapppington/tg_crypto_bot)
2. Нажмите кнопку **Fork** (справа вверху)
3. Выберите свой аккаунт — репозиторий скопируется в ваш профиль

### 6. Клонирование репозитория

Склонируйте свой форк на компьютер:
```bash
git clone https://github.com/ВАШ_ЛОГИН/tg_crypto_bot.git
cd tg_crypto_bot
```

### 7. Формат коммитов

Используйте префиксы для коммитов:
- `feat:` — новая функциональность
- `fix:` — исправление ошибки
- `refactor:` — рефакторинг кода
- `chore:` — обновление зависимостей, настройка проекта

**Примеры:**
```bash
git commit -m "feat: добавить функцию регистрации пользователя"
git commit -m "fix: исправить ошибку получения цены из API"
git commit -m "refactor: упростить код работы с БД"
git commit -m "chore: обновить requirements.txt"
```

---

## 🚀 Запуск проекта

1. Создайте бота через [@BotFather](https://t.me/BotFather) и получите токен
2. Установите зависимости
3. Создайте файл `.env` и укажите токен бота:
   ```env
   TELEGRAM_BOT_TOKEN=your_bot_token_here
   DATABASE_PATH=bot.db
   BINANCE_API_URL=https://api.binance.com
   ```
4. Запустите бота: `python main.py`

---

## 📝 Примечания

- Все цены отображаются в долларах США (USDT)
- Тикеры должны быть в верхнем регистре (BTC, ETH, SOL)
- Бот проверяет наличие тикера в таблице `supported_coins` перед запросом к API
- При ошибках API Binance бот должен корректно обрабатывать и сообщать пользователю
