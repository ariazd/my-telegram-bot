from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# توکن ربات که از BotFather گرفتی
TOKEN = "8278921645:AAEr6KC934DO4qn6QXYbqmSSSFx0DyxmPpQ"

# متن آماده
REPLY_TEXT = (
    "سلام 🌹\n"
    "من دستیار آریا هستم.\n"
    "فعلاً آریا قادر به پاسخگویی نیست، "
    "در اولین فرصت جواب شما رو خواهد داد.\n"
    "با تشکر 🙏"
)

# لیست استیکرها (file_id استیکرها)
STICKERS = [
    "CAACAgIAAxkBAAEBE1ZnKXJ7xWfQW9e4dPYG3N7-dUM3UgACrQADVp29Chdw4dbqzCqZNgQ",  
    "CAACAgIAAxkBAAEBE1hnKXJ_zXwWUMF3DqJxg3vP-t2F8wACwAIAAladvQp6XlA4J2ybYTQE",
]

# تابع جواب خودکار
async def auto_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # متن
    await update.message.reply_text(REPLY_TEXT)

    # استیکرها
    for s in STICKERS:
        await update.message.reply_sticker(s)

def main():
    app = Application.builder().token(TOKEN).build()

    # هر پیامی (غیر از دستورات /)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_reply))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
