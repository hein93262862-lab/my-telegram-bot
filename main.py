import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import google.generativeai as genai

TELEGRAM_TOKEN = "8898620118:AAGczTforK4nk0ljzuspNSUSmr3wvshPbOQ"
GOOGLE_API_KEY = "AQ.Ab8RN6IU6lG5s1-k-we7lckaZip_8SlU263guPV33o_PJ-INCw"

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="မင်္ဂလာပါ! ကျွန်တော် AI Bot ပါ။")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    try:
        response = model.generate_content(user_text)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=response.text)
    except Exception as e:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="ခွင့်လွှတ်ပါ၊ အမှားတစ်ခုခုဖြစ်နေလို့ပါ။")

if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), chat))

    print("Bot is running...")
    application.run_polling()
