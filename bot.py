import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import openai
import asyncio

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

API_KEY = os.getenv("API_KEY")  # OpenAI API Key
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
MODEL = os.getenv("MODEL", "gpt-3.5-turbo")

openai.api_key = API_KEY

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi! I am your GPT-4.5 Telegram Bot. Send me any message.")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    await update.message.chat.send_action(action="typing")
    try:
        response = await openai.ChatCompletion.acreate(
            model=MODEL,
            messages=[{"role": "user", "content": user_message}],
            max_tokens=500,
            temperature=0.7,
        )
        reply = response.choices[0].message.content
    except Exception as e:
        reply = f"Error: {e}"

    await update.message.reply_text(reply)

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), chat))

    print("Bot started...")
    app.run_polling()

if __name__ == "__main__":
    main()
