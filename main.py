import os
import logging
from flask import Flask
from threading import Thread
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
import google.generativeai as genai

# 1. Environment Variables မှ Key များကို ခေါ်ယူခြင်း (လုံခြုံရေးအတွက်)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Flask Setup
app = Flask(__name__)
@app.route('/')
def hello():
    return "Bot is running"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# Gemini Setup
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

async def start(update, context):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="မင်္ဂလာပါ! ကျွန်တော် AI Bot ပါ။")

async def chat(update, context):
    try:
        response = model.generate_content(update.message.text)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=response.text)
    except Exception as e:
        # အမှားကို Log ထဲမှာ မြင်ရအောင် print ထုတ်ပေးပါ
        print(f"Error: {e}")
        await context.bot.send_message(chat_id=update.effective_chat.id, text="ခဏစောင့်ပေးပါ၊ ပြန်ကြိုးစားကြည့်ပါ။")

if __name__ == '__main__':
    Thread(target=run_flask).start()
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), chat))
    application.run_polling()
