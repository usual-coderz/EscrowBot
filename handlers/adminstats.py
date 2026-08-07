from pyrogram import Client, filters
from datetime import datetime, timezone

from database import trades


@Client.on_message(filters.command("adminstats"))
async def admin_stats(client, message):

    username = (
        "@" + message.from_user.username
        if message.from_user.username
        else None
    )

    if not username:
        return await message.reply(
            "Username required."
        )


    total = 0
    volume = 0
    highest = 0
    ongoing = 0
    completed = 0


    today = datetime.utcnow().date()


    async for trade in trades.find(
        {
            "admin": username
        }
    ):

        amount = float(
            trade.get("amount",0)
        )

        total += 1
        volume += amount

        highest = max(
            highest,
            amount
        )

        if trade.get("status") == "ACTIVE":
            ongoing += 1

        if trade.get("status") == "RELEASED":
            completed += 1


    today_total = 0
    today_volume = 0


    async for trade in trades.find(
        {
            "admin": username
        }
    ):

        created = trade.get("created_at")

        if created and created.date() == today:
            today_total += 1
            today_volume += float(
                trade.get("amount",0)
            )


    await message.reply(
        f"""📊 Escrow Admin Stats

👤 Admin: {username}

📅 Today's Stats

🔢 Total Deals: {today_total}
💰 Total Volume: ${today_volume:.2f}

📊 All Time

🔢 Total Deals: {total}
💰 Total Volume: ${volume:.2f}
⚡ Highest Deal: ${highest:.2f}
⏳ Ongoing: {ongoing}
✅ Completed: {completed}
"""
    )