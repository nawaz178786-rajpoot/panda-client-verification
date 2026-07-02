# Text received
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

    if not all(field in data for field in required):
        await update.message.reply_text(
            "❌ Invalid format.\n\n"
            "Example:\n\n"
            "Name: John Doe\n"
            "Facebook: john123\n"
            "Instagram: john_insta\n"
            "Threads: johnthreads\n"
            "Age: 28\n"
            "Profession: Business\n"
            "Address: New York"
        )
        return

    context.user_data["client_data"] = data

    await update.message.reply_text("📷 Now send the client's photo.")