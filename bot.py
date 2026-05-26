import os
import telebot

TOKEN = os.environ.get('5740250067:AAEblxCJ-9FplsmagEdJ_Ui VNC3QemDVVsU) 
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Bot is online! I'm working even though your account is banned.")

bot.infinity_polling()