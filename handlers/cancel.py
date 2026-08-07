from pyrogram import Client, filters
from database import admins, trades


@Client.on_message(filters.command("cancel"))
async def cancel_trade(client, message):

    settings = await admins.find_one(
        {"chat_id": message.chat.id}
    )

    if not settings:
        return

    if (message.from_user.username or "").lower() != settings["username"].replace("@","").lower():
        return

    if len(message.command) != 2:
        return await message.reply(
            "Usage:\n/cancel <trade_id>"
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

    await trades.update_one(
        {"trade_id": trade_id},
        {
            "$set":{
                "status":"CANCELLED"
            }
        }
    )

    await message.reply(
        f"""Deal Cancelled

Trade ID: {trade_id}

Status: CANCELLED

Escrowed By: {settings['username']}
"""
    )