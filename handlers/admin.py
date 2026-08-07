from pyrogram import Client, filters
from database import admins

@Client.on_message(filters.command("setadmin"))
async def set_admin(client, message):

    if len(message.command) != 4:
        return await message.reply(
            "Usage:\n/setadmin <wallet> <approve_word> <username>"
        )

    wallet = message.command[1]
    approve = message.command[2]
    username = message.command[3]

    await admins.update_one(
        {"chat_id": message.chat.id},
        {
            "$set": {
                "wallet": wallet,
                "approve": approve,
                "username": username
            }
        },
        upsert=True
    )

    await message.reply(
        f"""✅ Escrow Admin Saved

Wallet:
`{wallet}`

Approve Word:
{approve}

Escrow Admin:
{username}
"""
    )