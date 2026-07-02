from telegram import Update
from telegram.ext import ContextTypes

from database import add_client, client_exists


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

    # ===========================
    # PHOTO
    # ===========================

    if update.message.photo:

        if "client_data" not in context.user_data:
            await update.message.reply_text(
                "❌ Please send client information first."
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
            client["notes"],
            file_id,
            update.effective_user.id,
            update.effective_user.full_name,
        )

        context.user_data.clear()

        await update.message.reply_text(
            "✅ Client saved successfully."
        )

        return

    # ===========================
    # TEXT
    # ===========================

    if update.message.text:

        try:

            data = {}

            for line in update.message.text.split("\n"):

                if ":" not in line:
                    continue

                key, value = line.split(":", 1)

                data[key.strip().lower()] = value.strip()

            facebook = data.get("facebook", "")
            instagram = data.get("instagram", "")
            threads = data.get("threads", "")

            existing = client_exists(
                facebook,
                instagram,
                threads,
            )

            if existing:

                await update.message.reply_text(
                    "❌ Client already exists."
                )

                return

            context.user_data["client_data"] = {

                "name": data.get("name", ""),
                "facebook": facebook,
                "instagram": instagram,
                "threads": threads,
                "age": data.get("age", ""),
                "profession": data.get("profession", ""),
                "address": data.get("address", ""),
                "notes": data.get("notes", ""),

            }

            await update.message.reply_text(
                "📷 Now send the client's photo."
            )

        except Exception:

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