from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
)

from config import BOT_TOKEN
from handlers import start, message_handler
from database import create_tables

print("🚀 Bot Started...")

# Create the database table if it doesn't exist
create_tables()

app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))

app.add_handler(
    MessageHandler(
        filters.TEXT | filters.PHOTO,
        message_handler,
    )
)

app.run_polling(drop_pending_updates=True)