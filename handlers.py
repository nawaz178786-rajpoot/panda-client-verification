import traceback

from telegram import Update
from telegram.ext import ContextTypes

from database import (
    add_client,
    client_exists,
    search_client,
)
from config import GROUP_ID


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to Panda Client Verification Bot!\n\n"
        "Send client information like this:\n\n"
        "Name: John Doe\n"
        "Facebook: john123\n"
        "Instagram: john_insta\n"
        "Threads: johnthreads\n"
        "Age: 28\n"
        "Profession: Business\n"
        "Address: New York\n"
        "Notes: VIP Client\n\n"
        "Then send the client's photo."
    )


async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None:
        return

    # Ignore commands like /search and /start
    if update.message.text and update.message.text.startswith("/"):
        return

    try:

        # ==========================
        # PHOTO RECEIVED
        # ==========================
        if update.message.photo:

            if "client_data" not in context.user_data:
                await update.message.reply_text(
                    "❌ Please send the client information first."
                )
                return

            photo = update.message.photo[-1]
            file_id = photo.file_id

            client = context.user_data["client_data"]

            add_client(
                client["name"],
                client["facebook"],
                client["instagram"],
                client["threads"],
                client["age"],
                client["profession"],
                client["address"],
                client.get("notes", ""),
                file_id,
                update.effective_user.id,
                update.effective_user.full_name,
            )

            caption = (
                "✅ NEW CLIENT ADDED\n\n"
                f"👤 Name: {client['name']}\n"
                f"📘 Facebook: {client['facebook']}\n"
                f"📸 Instagram: {client['instagram']}\n"
                f"🧵 Threads: {client['threads']}\n"
                f"🎂 Age: {client['age']}\n"
                f"💼 Profession: {client['profession']}\n"
                f"📍 Address: {client['address']}\n"
                f"📝 Notes: {client.get('notes', '-')}\n\n"
                f"👮 Added By: {update.effective_user.full_name}"
            )

            try:
                await context.bot.send_photo(
                    chat_id=GROUP_ID,
                    photo=file_id,
                    caption=caption,
                )
                print("✅ Photo sent to group successfully.")

            except Exception as group_error:
                print("========== GROUP SEND ERROR ==========")
                traceback.print_exc()
                print("GROUP_ID:", GROUP_ID)
                print("ERROR:", group_error)
                print("======================================")

            context.user_data.clear()

            await update.message.reply_text(
                "✅ Client saved successfully!"
            )
            return

        # ==========================
        # TEXT RECEIVED
        # ==========================
        if update.message.text:

            text = update.message.text.strip()

            data = {}

            for line in text.splitlines():

                if ":" not in line:
                    continue

                key, value = line.split(":", 1)

                data[key.strip().lower()] = value.strip()

            required = [
                "name",
                "facebook",
                "instagram",
                "threads",
                "age",
                "profession",
                "address",
            ]

            missing = [field for field in required if field not in data]

            if missing:
                await update.message.reply_text(
                    "❌ Invalid format.\n\n"
                    "Example:\n\n"
                    "Name: John Doe\n"
                    "Facebook: john123\n"
                    "Instagram: john_insta\n"
                    "Threads: johnthreads\n"
                    "Age: 28\n"
                    "Profession: Business\n"
                    "Address: New York\n"
                    "Notes: VIP Client"
                )
                return

            existing = client_exists(
                facebook=data.get("facebook", ""),
                instagram=data.get("instagram", ""),
                threads=data.get("threads", ""),
            )

            if existing:
                await update.message.reply_text(
                    "⚠️ Client already exists in the database.\n\n"
                    "This client cannot be added again."
                )
                return

            context.user_data["client_data"] = {
                "name": data.get("name", ""),
                "facebook": data.get("facebook", ""),
                "instagram": data.get("instagram", ""),
                "threads": data.get("threads", ""),
                "age": data.get("age", ""),
                "profession": data.get("profession", ""),
                "address": data.get("address", ""),
                "notes": data.get("notes", ""),
            }

            await update.message.reply_text(
                "📷 Now send the client's photo."
            )

    except Exception:
        traceback.print_exc()

        await update.message.reply_text(
            "❌ An unexpected error occurred. Check Railway logs."
        )


# ====================================
# SEARCH CLIENT
# ====================================

async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if len(context.args) == 0:
        await update.message.reply_text(
            "Usage:\n/search username"
        )
        return

    keyword = " ".join(context.args).strip()

    client = search_client(keyword)

    if client is None:
        await update.message.reply_text(
            f"❌ No client found for:\n{keyword}"
        )
        return

    caption = (
        "🔍 CLIENT FOUND\n\n"
        f"👤 Name: {client['name']}\n"
        f"📘 Facebook: {client['facebook']}\n"
        f"📸 Instagram: {client['instagram']}\n"
        f"🧵 Threads: {client['threads']}\n"
        f"🎂 Age: {client['age']}\n"
        f"💼 Profession: {client['profession']}\n"
        f"📍 Address: {client['address']}\n"
        f"📝 Notes: {client['notes']}\n"
        f"👮 Added By: {client['added_by_name']}\n"
        f"📅 Added: {client['created_at']}"
    )

    if client["photo"]:
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=client["photo"],
            caption=caption,
        )
    else:
        await update.message.reply_text(caption)