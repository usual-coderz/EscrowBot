from pyrogram import Client, filters
from database import admins


@Client.on_message(filters.command("setadmin"))
async def set_admin(client, message):

    if len(message.command) != 4:
        return await message.reply(
            "Usage:\n"
            "/setadmin <wallet_address> <approve_word> <@username>"
        )

    wallet = message.command[1].strip()
    approve = message.command[2].strip().upper()
    username = message.command[3].strip().lower()

    if not username.startswith("@"):
        username = "@" + username

    await admins.update_one(
        {"chat_id": message.chat.id},
        {
            "$set": {
                "chat_id": message.chat.id,
                "wallet": wallet,
                "approve": approve,
                "username": username
            }
        },
        upsert=True
    )

    await message.reply(
        f"""<b>Escrow Settings Saved</b>

<b>Group ID:</b> <code>{message.chat.id}</code>

<b>Admin:</b> {username}

<b>Approve Word:</b> <code>{approve}</code>

<b>Wallet Address:</b>

<pre>{wallet}</pre>
""",
        parse_mode="html"
    )


@Client.on_message(filters.command("admin"))
async def show_admin(client, message):

    data = await admins.find_one({"chat_id": message.chat.id})

    if not data:
        return await message.reply("No escrow settings found for this group.")

    await message.reply(
        f"""<b>Escrow Settings</b>

<b>Group ID:</b> <code>{data['chat_id']}</code>

<b>Admin:</b> {data['username']}

<b>Approve Word:</b> <code>{data['approve']}</code>

<b>Wallet Address:</b>

<pre>{data['wallet']}</pre>
""",
        parse_mode="html"
    )