from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
)

from config import BOT_TOKEN
from handlers import (
    start,
    message_handler,
    search,
)
from database import create_tables

print("🚀 Bot Started...")

# Create database tables
create_tables()

# Create bot
app = Application.builder().token(BOT_TOKEN).build()

# =====================================
# COMMANDS
# =====================================

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("search", search))

# =====================================
# MESSAGE HANDLER
# =====================================

app.add_handler(
    MessageHandler(
        filters.TEXT | filters.PHOTO,
        message_handler,
    )
)

# =====================================
# START BOT
# =====================================

app.run_polling(drop_pending_updates=True)