"""
ТеорМех Бот — Telegram Mini App
Хостинг: Railway (24/7)
"""

import os
import telebot
from telebot.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    MenuButtonWebApp,
    WebAppInfo,
)

# ── НАСТРОЙКИ (берутся из переменных окружения Railway) ──
BOT_TOKEN    = os.environ.get("BOT_TOKEN", "")
MINI_APP_URL = os.environ.get("MINI_APP_URL", "")

if not BOT_TOKEN:
    raise ValueError("Переменная BOT_TOKEN не задана!")
if not MINI_APP_URL:
    raise ValueError("Переменная MINI_APP_URL не задана!")

bot = telebot.TeleBot(BOT_TOKEN)


def main_kb():
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(
            text="⚙️ Открыть ТеорМех Бот",
            web_app=WebAppInfo(url=MINI_APP_URL),
        )
    )
    return markup


@bot.message_handler(commands=["start"])
def cmd_start(message):
    name = message.from_user.first_name or "студент"
    bot.send_message(
        message.chat.id,
        f"👋 Привет, {name}!\n\n"
        "Я решаю задачи по *теоретической механике*:\n"
        "• 📐 Статика — равновесие, фермы, рамы\n"
        "• 🔄 Кинематика — скорости, ускорения, МЦС\n"
        "• 💥 Динамика — уравнения движения, энергия\n\n"
        "Загрузи фото задачи или введи условие — решу пошагово и нарисую схему.\n\n"
        "👇 Нажми кнопку:",
        parse_mode="Markdown",
        reply_markup=main_kb(),
    )


@bot.message_handler(commands=["app"])
def cmd_app(message):
    bot.send_message(message.chat.id, "⚙️ Открывай:", reply_markup=main_kb())


@bot.message_handler(commands=["help"])
def cmd_help(message):
    bot.send_message(
        message.chat.id,
        "📚 *Как пользоваться:*\n\n"
        "1. Нажми *Открыть ТеорМех Бот*\n"
        "2. Введи условие или загрузи фото задачи\n"
        "3. Выбери режим: Решить / Проверить / Схема\n"
        "4. Получи решение + Canvas-схему\n\n"
        "/start — главное меню\n"
        "/app — открыть приложение",
        parse_mode="Markdown",
        reply_markup=main_kb(),
    )


@bot.message_handler(content_types=["text", "photo", "document"])
def handle_any(message):
    bot.send_message(
        message.chat.id,
        "👇 Открой приложение — там можно загрузить фото и решить задачу:",
        reply_markup=main_kb(),
    )


def setup_menu_button():
    try:
        bot.set_chat_menu_button(
            menu_button=MenuButtonWebApp(
                text="⚙️ ТеорМех",
                web_app=WebAppInfo(url=MINI_APP_URL),
            )
        )
        print("✅ Кнопка меню установлена")
    except Exception as e:
        print(f"⚠️  Кнопка меню: {e}")


if __name__ == "__main__":
    print("🚀 ТеорМех Бот запущен (Railway 24/7)")
    print(f"📱 Mini App: {MINI_APP_URL}")
    setup_menu_button()
    bot.infinity_polling(timeout=30, long_polling_timeout=30)
