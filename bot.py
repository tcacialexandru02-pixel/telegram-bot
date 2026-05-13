import json
import random
import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    ContextTypes,
    filters,
)

import os

TOKEN = os.getenv("TOKEN")

DB_FILE = "messages.json"

# Загружаем сообщения
if os.path.exists(DB_FILE):
    with open(DB_FILE, "r", encoding="utf-8") as f:
        messages = json.load(f)
else:
    messages = []


# Сохраняем сообщения
def save_messages():
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)


# Обработка сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global messages

    text = update.message.text

    # Игнорируем слишком короткие сообщения
if len(text) < 4:
    return

# Игнорируем ссылки
if "http" in text:
    return

    # Сохраняем сообщение
    messages.append(text)

    # Ограничение памяти
    if len(messages) > 5000:
        messages = messages[-5000:]

    save_messages()

    # Шанс 35% повторить старое сообщение
    if random.randint(1, 100) <= 35:
        random_message = random.choice(messages)

        await update.message.reply_text(random_message)


# Запуск
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
)

print("Бот запущен!")

app.run_polling()
