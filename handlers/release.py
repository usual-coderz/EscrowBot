from pyrogram import Client, filters
from pyrogram.enums import ParseMode

from database import admins, trades


@Client.on_message(filters.command("release"))
async def release_trade(client, message):

    settings = await admins.find_one(
        {"chat_id": message.chat.id}
    )

    if not settings:
        return

    # Only escrow admin
    if (
        (message.from_user.username or "").lower()
        != settings["username"].replace("@", "").lower()
    ):
        return

    if len(message.command) != 2:
        return await message.reply(
            "Usage:\n/release <trade_id>"
        )

    trade_id = message.command[1]

    trade = await trades.find_one(
        {
            "trade_id": trade_id,
            "chat_id": message.chat.id
        }
    )

    if not trade:
        return await message.reply(
            "Trade not found."
        )

    if trade.get("status") != "ACTIVE":
        return await message.reply(
            f"Trade already {trade.get('status')}"
        )

    await trades.update_one(
        {
            "trade_id": trade_id,
            "chat_id": message.chat.id
        },
        {
            "$set": {
                "status": "RELEASED"
            }
        }
    )

    amount = trade.get("release_amount", 0)

    await message.reply(
        f"""<b>Deal Released</b>

<b>Trade ID:</b> <code>{trade_id}</code>

<b>Amount:</b> ${amount:.2f}

<b>Buyer:</b> {trade.get("buyer", "-")}
<b>Seller:</b> {trade.get("seller", "-")}

<b>Status:</b> RELEASED

<b>Escrowed By:</b> {settings.get("username", "-")}

<code>Vouch @stocknfts for ${amount:.2f} smooth and trusted deal.</code>""",
        parse_mode=ParseMode.HTML
    )