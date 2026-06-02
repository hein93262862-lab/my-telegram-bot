import logging
import os
from flask import Flask
from threading import Thread
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
import google.generativeai as genai

# Flask App တည်ဆောက်ခြင်း
app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is running"

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

# Telegram Bot Setup
TELEGRAM_TOKEN = "8898620118:AAGWpDwR0q-XrA2h61Yv0zwwpmzvdbE0tw8"
GOOGLE_API_KEY = "AQ.Ab8RN6K3o9tMQAkh7KLbbnAanaCJGYk12p7A2bWD87ANaFIW_g"

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

async def start(update, context):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="မင်္ဂလာပါ! ကျွန်တော် AI Bot ပါ။")

async def chat(update, context):
    try:
        response = model.generate_content(update.message.text)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=response.text)
    except:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="အမှားတစ်ခုခုဖြစ်နေပါတယ်။")

if __name__ == '__main__':
    # Flask ကို Background မှာ အလုပ်လုပ်ခိုင်းခြင်း
    Thread(target=run_flask).start()
    
    # Telegram Bot ကို စတင်ခြင်း
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), chat))
    application.run_polling()    
