from pyrogram import Client, filters
from pyrogram.enums import ParseMode

from database import trades


@Client.on_message(filters.command("deals"))
async def deals(client, message):

    target = None

    # Reply Mode
    if message.reply_to_message and message.reply_to_message.from_user:

        user = message.reply_to_message.from_user

        if user.username:
            target = f"@{user.username.lower()}"
        else:
            target = str(user.id)

    # Command Mode
    elif len(message.command) == 2:

        target = message.command[1].strip().lower()

        if not target.startswith("@") and not target.isdigit():
            target = "@" + target

    else:
        return await message.reply(
            "Usage:\n"
            "/deals @username\n"
            "/deals user_id\n\n"
            "or reply to a user's message with /deals"
        )

    text = "<b>ACTIVE DEALS</b>\n\n"
    count = 0

    async for trade in trades.find({"status": "ACTIVE"}):

        buyer = str(trade.get("buyer", "")).strip().lower()
        seller = str(trade.get("seller", "")).strip().lower()

        if target != buyer and target != seller:
            continue

        count += 1

        text += (
            f"<b>{count}.</b> <code>{trade['trade_id']}</code>\n"
            f"<b>Amount:</b> ${trade.get('amount', 0):.2f}\n"
            f"<b>Buyer:</b> {trade.get('buyer', '-')}\n"
            f"<b>Seller:</b> {trade.get('seller', '-')}\n"
            f"<b>Escrow:</b> {trade.get('escrow_admin', '-')}\n\n"
        )

    if count == 0:
        return await message.reply(
            "No active deals found."
        )

    await message.reply(
        text,
        parse_mode=ParseMode.HTML
    )