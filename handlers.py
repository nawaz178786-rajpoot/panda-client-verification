async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    print("========== UPDATE ==========")
    print(update)

    if update.effective_chat:
        print("GROUP ID =", update.effective_chat.id)
        print("GROUP NAME =", update.effective_chat.title)

    await update.message.reply_text("✅ Bot Connected Successfully")

    text = update.message.text

    try:
        lines = text.split("\n")

        data = {}

        for line in lines:
            key, value = line.split(":", 1)
            data[key.strip().lower()] = value.strip()

        context.user_data["client_data"] = {
            "name": data.get("name", ""),
            "facebook": data.get("facebook", ""),
            "instagram": data.get("instagram", ""),
            "threads": data.get("threads", ""),
            "age": data.get("age", ""),
            "profession": data.get("profession", ""),
            "address": data.get("address", "")
        }

        await update.message.reply_text("📷 Now send the client's photo.")

    except Exception:
        await update.message.reply_text("❌ Invalid format.")