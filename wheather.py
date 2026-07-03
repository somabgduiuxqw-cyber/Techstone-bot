"""
------------------------------------------------------------------
Weather Bot Pro - ATP Network Production Build (Fixed Edition)
------------------------------------------------------------------
"""
import telebot
import requests

# --- 1. CORE CONFIGURATION ---
# Make sure to place your fresh, secure token here
TELEGRAM_TOKEN = '8459995374:AAEJpDrS6TDZ8v4JP3NCgb-b9HdutHErE28'
WEATHER_API_KEY = '2c7cb5201d87d2ffc1ce0b3c15708f0f'
OWNER_ID = 8686609563

# --- 2. STATE MANAGEMENT ---
is_maintenance_mode = False

bot = telebot.TeleBot(TELEGRAM_TOKEN)
print("🚀 ATP Network Weather Bot engine initialized smoothly with HTML Parsing...")


# --- 3. OWNER ADMIN COMMANDS ---

@bot.message_handler(commands=['stop'])
def stop_bot(message):
    global is_maintenance_mode
    if message.from_user.id != OWNER_ID:
        return
    
    is_maintenance_mode = True
    bot.reply_to(message, "🔧 <b>Maintenance Mode Activated.</b> All public operations are paused.", parse_mode='HTML')


@bot.message_handler(commands=['reset'])
def reset_bot(message):
    global is_maintenance_mode
    if message.from_user.id != OWNER_ID:
        return
    
    is_maintenance_mode = False
    bot.reply_to(message, "🔄 <b>Bot Reset.</b> System parameters cleared and set to default (Online).", parse_mode='HTML')


@bot.message_handler(commands=['start'])
def send_welcome(message):
    if is_maintenance_mode and message.from_user.id != OWNER_ID:
        bot.reply_to(message, "⚠️ <i>Bot is under maintenance.</i>\n\nPlease check back later. We are currently performing updates.", parse_mode='HTML')
        return

    # HTML tags avoid any parsing errors with underscores
    welcome_text = (
        "<b>Hello!</b> 🌤️\n\n"
        "Send me any global location (City, State, or Country) to get an instant weather report.\n\n"
        "------------------------------------------\n"
        "🛠️ <b>Script developed by:</b> ATP Network\n"
        "💬 <b>Support/Contact:</b> @atp_network\n"
        "------------------------------------------"
    )
    bot.reply_to(message, welcome_text, parse_mode='HTML')


# --- 4. GLOBAL MESSAGE PROCESSING ---
@bot.message_handler(func=lambda message: True)
def handle_weather_request(message):
    if message.text.startswith('/'):
        return

    if is_maintenance_mode and message.from_user.id != OWNER_ID:
        bot.reply_to(message, "⚠️ <i>Bot is under maintenance.</i>\n\nPlease check back later.", parse_mode='HTML')
        return

    bot.send_chat_action(message.chat.id, 'typing')

    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={requests.utils.quote(message.text)}&appid={WEATHER_API_KEY}&units=metric"
        response = requests.get(url).json()

        # Build clean HTML text response
        report = (
            f"📍 <b>Weather in {response['name']}, {response['sys']['country']}</b>\n"
            f"-----------------------------------------\n"
            f"<b>Condition:</b> {response['weather'][0]['description'].title()}\n"
            f"🌡️ <b>Temp:</b> {response['main']['temp']}°C\n"
            f"💧 <b>Humidity:</b> {response['main']['humidity']}%\n\n"
            f"<i>Developed by ATP Network</i>"
        )
        bot.reply_to(message, report, parse_mode='HTML')

    except Exception as e:
        print(f"Fetch Error: {e}")
        bot.reply_to(message, "❌ <b>Location not found.</b>\n\nPlease try again or contact @atp_network if the issue persists.", parse_mode='HTML')


if __name__ == '__main__':
    bot.infinity_polling()
