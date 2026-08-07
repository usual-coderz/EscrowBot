from pyrogram import Client, filters
from database import admins


@Client.on_message(filters.command("setadmin"))
async def set_admin(client, message):

    # Sirf group me allow
    if message.chat.type not in ["group", "supergroup"]:
        return await message.reply("❌ Use this command in a group.")

    if len(message.command) != 4:
        return await message.reply(
            "Usage:\n"
            "/setadmin <wallet> <approve_word> <@username>\n\n"
            "Example:\n"
            "/setadmin TVxxxxxxxxxxxxxxxx P @icivan"
        )

    wallet = message.command[1].strip()
    approve = message.command[2].strip().upper()
    username = message.command[3].strip()

    if not username.startswith("@"):
        return await message.reply("❌ Username must start with @")

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
        f"""✅ Escrow Admin Configured

👤 Admin : {username}
💰 Wallet : `{wallet}`
🔑 Approve Word : {approve}
"""
    )


@Client.on_message(filters.command("admin"))
async def show_admin(client, message):

    data = await admins.find_one({"chat_id": message.chat.id})

    if not data:
        return await message.reply("❌ No admin configured.")

    await message.reply(
        f"""🛡 Escrow Settings

👤 Admin : {data['username']}
💰 Wallet : `{data['wallet']}`
🔑 Approve Word : {data['approve']}
"""
    )