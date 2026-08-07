from pyrogram import Client, filters
from pyrogram.enums import ChatType, ParseMode

from config import OWNER_ID
from database import admins


@Client.on_message(filters.command("setadmin"))
async def set_admin(client, message):

    if message.from_user.id != OWNER_ID:
        return await message.reply("You are not authorized to use this command.")

    if message.chat.type not in (ChatType.GROUP, ChatType.SUPERGROUP):
        return await message.reply("This command can only be used in groups.")

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
                "chat_title": message.chat.title or "Unknown",
                "wallet": wallet,
                "approve": approve,
                "username": username
            }
        },
        upsert=True
    )

    await message.reply(
        f"""<b>Escrow Settings Saved</b>

<b>Group:</b> {message.chat.title or "Unknown"}
<b>Chat ID:</b> <code>{message.chat.id}</code>

<b>Admin:</b> {username}
<b>Approve Word:</b> <code>{approve}</code>

<b>Wallet Address:</b>

<pre>{wallet}</pre>
""",
        parse_mode=ParseMode.HTML
    )


@Client.on_message(filters.command("admin"))
async def show_admin(client, message):

    data = await admins.find_one({"chat_id": message.chat.id})

    if not data:
        return await message.reply("No escrow settings found for this group.")

    await message.reply(
        f"""<b>Escrow Settings</b>

<b>Group:</b> {data.get("chat_title", "Unknown")}
<b>Chat ID:</b> <code>{data['chat_id']}</code>

<b>Admin:</b> {data['username']}
<b>Approve Word:</b> <code>{data['approve']}</code>

<b>Wallet Address:</b>

<pre>{data['wallet']}</pre>
""",
        parse_mode=ParseMode.HTML
    )


@Client.on_message(filters.command("admins"))
async def list_admins(client, message):

    if message.from_user.id != OWNER_ID:
        return

    text = "<b>Escrow Groups</b>\n\n"
    count = 0

    async for data in admins.find():
        count += 1
        text += (
            f"<b>{count}.</b> {data.get('chat_title', 'Unknown')}\n"
            f"<b>Chat ID:</b> <code>{data['chat_id']}</code>\n"
            f"<b>Admin:</b> {data['username']}\n"
            f"<b>Approve:</b> <code>{data['approve']}</code>\n\n"
        )

    if count == 0:
        text += "No groups found."

    await message.reply(text, parse_mode=ParseMode.HTML)


@Client.on_message(filters.command("deladmin"))
async def del_admin(client, message):

    if message.from_user.id != OWNER_ID:
        return

    if len(message.command) != 2:
        return await message.reply("Usage:\n/deladmin <chat_id>")

    try:
        chat_id = int(message.command[1])
    except ValueError:
        return await message.reply("Invalid Chat ID.")

    result = await admins.delete_one({"chat_id": chat_id})

    if result.deleted_count:
        await message.reply("Escrow settings deleted successfully.")
    else:
        await message.reply("No settings found for that Chat ID.")