import logging
import google.generativeai as genai
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- CONFIGURATION ---
TELEGRAM_TOKEN = "8015832524:AAHKa3jxXSn1q7glqLlMEpDx3iMzfo58pF4"
GEMINI_API_KEY = "AIzaSyDfr10tWM7eAYxTfr5rhwd4KBVkbgX4s2k"

# Gemini AI Setup
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

# Auto Send Message Content
AUTO_MSG = """
*PTERODACTYL ADMIN PANEL* ⚡ CPU : UNLIMITED  🙀🚀
⚡ MEMORY : UNLIMITED  😼🙌
⚡ SUPER FAST & SPEED  BOT DEVELOPMENT PANEL  

🚀 Speed • Power • Stability  
📩 Price & Details → Inbox

 *BENIFITS* ✅

* ANTI DELAY
* ANTI PROXY
* 30 DAY REPLACEMENT WARRANTY 
* 24/7 WORKING 
* FULL ACCESS 
* ANTI DDOS
* 24 NODE SUPPORT 


 *PRICE LIST*
* UNLIMITED PANEL - Rs 350
* ADMIN PANEL - Rs 1200
* PT PANEL RESELL ACCESS - Rs 2500
* OWNER PANEL - Rs 3500
* BUG BOT DEPLOY - Rs 350
* MD BOT DEPLOY - Rs 300

> CONTACT 
> TELEGRAM - https://t.me/CyberMitzii
"""

# --- FUNCTIONS ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the /start command"""
    keyboard = [[InlineKeyboardButton("Buy Now / Contact Admin", url="https://t.me/CyberMitzii")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"Hello {update.effective_user.first_name}! I am **Mitzii AI Bot**. How can I help you today?\n\nUse /price to see our hosting deals!",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def send_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends the price list to the user"""
    await update.message.reply_text(AUTO_MSG, parse_mode='Markdown')

async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Welcomes new members to the group"""
    for new_member in update.message.new_chat_members:
        if new_member.id == context.bot.id:
            continue
        
        name = new_member.first_name
        welcome_text = (
            f"Welcome {name} to *CyberMitzii*! 🚀\n\n"
            "We provide high-quality Pterodactyl Panels for your needs.\n"
            "Type /price to see our latest deals or click the button below."
        )
        await update.message.reply_text(welcome_text, parse_mode='Markdown')

async def handle_ai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles AI responses and keyword detection"""
    user_text = update.message.text
    if not user_text:
        return

    # Keyword Detection
    keywords = ["price", "panel", "buy", "hosting", "cost", "pannal", "how much"]
    if any(word in user_text.lower() for word in keywords):
        await send_price(update, context)
        return

    # AI Response for general chat
    try:
        response = model.generate_content(user_text)
        await update.message.reply_text(response.text)
    except Exception:
        pass

# --- MAIN ---

if __name__ == '__main__':
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Registering Handlers
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("price", send_price))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_ai))
    
    print("Mitzii Bot is starting...")
    application.run_polling()
