from pyrogram import Client, filters
from database import trades


@Client.on_message(filters.command("stats"))
async def user_stats(client, message):

    username = None

    # Reply mode
    if message.reply_to_message and message.reply_to_message.from_user:

        user = message.reply_to_message.from_user

        if not user.username:
            return await message.reply(
                "This user doesn't have a username."
            )

        username = f"@{user.username.lower()}"

    # Command mode
    elif len(message.command) == 2:

        username = message.command[1].strip().lower()

        if not username.startswith("@"):
            username = "@" + username

    else:
        return await message.reply(
            "Usage:\n"
            "/stats @username\n\n"
            "or reply to a user's message with /stats"
        )

    total_deals = 0
    total_volume = 0
    ongoing = 0
    highest = 0

    async for trade in trades.find():

        buyer = str(trade.get("buyer", "")).strip().lower()
        seller = str(trade.get("seller", "")).strip().lower()

        if username != buyer and username != seller:
            continue

        total_deals += 1

        amount = float(trade.get("amount", 0))

        total_volume += amount
        highest = max(highest, amount)

        if trade.get("status") == "ACTIVE":
            ongoing += 1

    if total_deals == 0:
        return await message.reply(
            f"No deals found for {username}"
        )

    # Ranking
    users = {}

    async for trade in trades.find():

        amount = float(trade.get("amount", 0))

        for user in [
            trade.get("buyer"),
            trade.get("seller")
        ]:

            if not user:
                continue

            user = str(user).strip().lower()

            users[user] = users.get(user, 0) + amount

    ranking = sorted(
        users.items(),
        key=lambda x: x[1],
        reverse=True
    )

    rank = "-"

    for i, (user, _) in enumerate(ranking, start=1):
        if user == username:
            rank = i
            break

    await message.reply(
        f"""📊 Participant Stats for {username}

👑 Ranking: #{rank}
📈 Total Volume: ${total_volume:.2f}
🔢 Total Deals: {total_deals}
⏳ Ongoing Deals: {ongoing}
⚡ Highest Deal: ${highest:.2f}

📊 Always use @TestEscrowerBot for safer transactions!"""
    )