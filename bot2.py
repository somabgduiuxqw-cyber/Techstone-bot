import os
import requests
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TELEGRAM_TOKEN = os.getenv("5740250067:AAEblxCJ-9FplsmagEdJ_Ui VNC3QemDVVsU")
TELEGRAPH_TOKEN = os.getenv("5740250067:AAEblxCJ-9FplsmagEdJ_Ui VNC3QemDVVsU")

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send /post Your text here to create a Telegraph page")

async def post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = " ".join(context.args)
    if not text:
        await update.message.reply_text("Usage: /post Your text here")
        return
    try:
        r = requests.post("https://api.telegra.ph/createPage", data={
            "access_token": 5740250067:AAEblxCJ-9FplsmagEdJ_Ui VNC3QemDVVsU,
            "title": "Telegram Post", 
            "author_name": "@Technostoneytbot",
            "content": '[{"tag":"p","children":["' + text.replace('"', '\\"') + '"]}]'
        }, timeout=10)
        data = r.json()
        if data.get("ok"):
            await update.message.reply_text(f"Done: {data['result']['url']}")
        else:
            await update.message.reply_text(f"Telegraph error: {data.get('error')}")
    except Exception as e:
        logging.error(e)
        await update.message.reply_text("Failed to create page.")

def main():
    app = ApplicationBuilder().token(5740250067:AAEblxCJ-9FplsmagEdJ_Ui VNC3QemDVVsU).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("post", post))
    app.run_polling()

if __name__ == "__main__":
    main()
