from pyrogram import Client, filters
from database import trades


@Client.on_message(filters.command("stats"))
async def user_stats(client, message):

    username = None

    # Reply mode
    if message.reply_to_message:

        user = message.reply_to_message.from_user

        if user and user.username:
            username = "@" + user.username


    # Command mode
    if not username and len(message.command) == 2:

        username = message.command[1]

        if not username.startswith("@"):
            username = "@" + username


    if not username:
        return await message.reply(
            "Usage:\n/stats @username\n\nOr reply to a user's message with /stats"
        )


    username_lower = username.lower()


    total_deals = 0
    total_volume = 0
    ongoing = 0
    highest = 0


    async for trade in trades.find():

        buyer = trade.get("buyer", "").lower()
        seller = trade.get("seller", "").lower()

        if username_lower not in [buyer, seller]:
            continue


        total_deals += 1

        amount = float(
            trade.get("amount", 0)
        )

        total_volume += amount

        highest = max(
            highest,
            amount
        )

        if trade.get("status") == "ACTIVE":
            ongoing += 1


    if total_deals == 0:
        return await message.reply(
            f"No deals found for {username}"
        )


    # Ranking
    users = {}

    async for trade in trades.find():

        amount = float(
            trade.get("amount", 0)
        )

        for user in [
            trade.get("buyer"),
            trade.get("seller")
        ]:

            if user:
                users[user.lower()] = (
                    users.get(user.lower(), 0)
                    + amount
                )


    ranking = sorted(
        users.items(),
        key=lambda x: x[1],
        reverse=True
    )


    rank = next(
        (
            i + 1
            for i, item in enumerate(ranking)
            if item[0] == username_lower
        ),
        "-"
    )


    await message.reply(
        f"""📊 Participant Stats for {username}

👑 Ranking: #{rank}
📈 Total Volume: ${total_volume:.2f}
🔢 Total Deals: {total_deals}
⏳ Ongoing Deals: {ongoing}
⚡ Highest Deal: ${highest:.2f}

📊 Always use @TestEscrowerBot for safer transactions!"""
    )