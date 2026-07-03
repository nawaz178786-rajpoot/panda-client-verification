
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
        "Send client information in the following format:\n\n"
        "Name: John Doe\n"
        "Facebook: john123\n"
        "Instagram: john_insta\n"
        "Threads: johnthreads\n"
        "Age: 28\n"
        "Profession: Business\n"
        "Education: MBA\n"
        "Marital Status: Married\n"
        "Address: New York\n"
        "Notes: VIP Client\n\n"
        "📷 After sending the information, send the client's photo."
    )


async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None:
        return

    if update.message.text and update.message.text.startswith("/"):
        return

    try:
        if update.message.photo:
            if "client_data" not in context.user_data:
                await update.message.reply_text("❌ Please send the client information first.")
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
                client["education"],
                client["marital_status"],
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
                f"🎓 Education: {client['education']}\n"
                f"💍 Marital Status: {client['marital_status']}\n"
                f"📍 Address: {client['address']}\n"
                f"📝 Notes: {client.get('notes','-')}\n\n"
                f"👮 Added By: {update.effective_user.full_name}"
            )

            try:
                await context.bot.send_photo(
                    chat_id=GROUP_ID,
                    photo=file_id,
                    caption=caption,
                )
                print("✅ Photo sent to group successfully.")
            except Exception:
                print("========== GROUP SEND ERROR ==========")
                traceback.print_exc()
                print("======================================")

            context.user_data.clear()
            await update.message.reply_text("✅ Client saved successfully!")
            return

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
                "education",
                "marital status",
                "address",
            ]

            missing = [f for f in required if f not in data]
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
                    "Education: MBA\n"
                    "Marital Status: Married\n"
                    "Address: New York\n"
                    "Notes: VIP Client"
                )
                return

            facebook = data.get("facebook","").strip()
            instagram = data.get("instagram","").strip()
            threads = data.get("threads","").strip()

            if not (facebook or instagram or threads):
                await update.message.reply_text(
                    "❌ Please provide at least one social media username (Facebook, Instagram or Threads)."
                )
                return

            existing = client_exists(facebook=facebook, instagram=instagram, threads=threads)
            if existing:
                await update.message.reply_text(
                    "⚠️ Client already exists in the database.\n\n"
                    f"👤 Name: {existing['name']}\n"
                    f"👮 Added By: {existing['added_by_name']}\n"
                    f"📅 Added: {existing['created_at']}\n\n"
                    "Use /search to view the complete client information."
                )
                return

            context.user_data["client_data"] = {
                "name": data.get("name","").strip(),
                "facebook": facebook,
                "instagram": instagram,
                "threads": threads,
                "age": data.get("age","").strip(),
                "profession": data.get("profession","").strip(),
                "education": data.get("education","").strip(),
                "marital_status": data.get("marital status","").strip(),
                "address": data.get("address","").strip(),
                "notes": data.get("notes","").strip(),
            }

            await update.message.reply_text("📷 Now send the client's photo.")

    except Exception:
        traceback.print_exc()
        await update.message.reply_text("❌ An unexpected error occurred. Check Railway logs.")


async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text("Usage:\n/search username")
        return

    keyword = " ".join(context.args).strip()
    client = search_client(keyword)

    if client is None:
        await update.message.reply_text(f"❌ No client found for:\n{keyword}")
        return

    caption = (
        "🔍 CLIENT FOUND\n\n"
        f"👤 Name: {client['name']}\n"
        f"📘 Facebook: {client['facebook']}\n"
        f"📸 Instagram: {client['instagram']}\n"
        f"🧵 Threads: {client['threads']}\n"
        f"🎂 Age: {client['age']}\n"
        f"💼 Profession: {client['profession']}\n"
        f"🎓 Education: {client['education']}\n"
        f"💍 Marital Status: {client['marital_status']}\n"
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
