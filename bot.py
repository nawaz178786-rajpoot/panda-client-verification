from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
)

from config import BOT_TOKEN
from handlers import start, message_handler

print("Bot Started...")

app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(
    MessageHandler(
        filters.ALL,
        message_handler
    )
)

app.run_polling(drop_pending_updates=True)