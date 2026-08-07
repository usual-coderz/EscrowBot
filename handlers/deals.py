from pyrogram import Client, filters
from database import trades
from pyrogram.enums import ParseMode


@Client.on_message(filters.command("deals"))
async def deals(client, message):

    target = None

    # Reply mode
    if message.reply_to_message and message.reply_to_message.from_user:
        user = message.reply_to_message.from_user

        if user.username:
            target = "@" + user.username.lower()
        else:
            target = str(user.id)

    # Command mode
    elif len(message.command) == 2:
        target = message.command[1].lower()

        if target.startswith("@"):
            pass
        elif target.isdigit():
            pass
        else:
            target = "@" + target

    else:
        return await message.reply(
            "Usage:\n"
            "/deals @username\n"
            "/deals user_id\n\n"
            "or reply to a user's message with /deals"
        )

    text = "<b>User Deals</b>\n\n"
    count = 0

    async for trade in trades.find():

        buyer = str(trade.get("buyer", "")).lower()
        seller = str(trade.get("seller", "")).lower()

        if target not in [buyer, seller]:
            continue

        count += 1

        text += (
            f"<b>{count}.</b> {trade['trade_id']}\n"
            f"Amount: ${trade['amount']:.2f}\n"
            f"Status: {trade['status']}\n"
            f"Buyer: {trade['buyer']}\n"
            f"Seller: {trade['seller']}\n"
            f"Escrow: {trade['escrow_admin']}\n\n"
        )

    if count == 0:
        return await message.reply("No deals found.")

    if len(text) > 4000:
        text = text[:3900] + "\n..."

    await message.reply(
    text,
    parse_mode=ParseMode.HTML
)