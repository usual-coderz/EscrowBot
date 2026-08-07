from pyrogram import Client, filters

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

    await message.reply(
        f"""Deal Released

Trade ID: {trade_id}

Amount: ${trade['release_amount']:.2f}

Buyer: {trade.get('buyer','-')}
Seller: {trade.get('seller','-')}

Status: RELEASED

Escrowed By: {settings['username']}
"""
    )