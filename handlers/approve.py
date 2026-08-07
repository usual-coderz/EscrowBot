from pyrogram import Client, filters
from pyrogram.enums import ParseMode

from database import admins


@Client.on_message(filters.reply & filters.text)
async def approve_deal(client, message):

    replied = message.reply_to_message

    if not replied or not replied.text:
        return

    settings = await admins.find_one({"chat_id": message.chat.id})

    if not settings:
        return

    # Only configured escrow admin
    username = (message.from_user.username or "").lower()
    admin_username = settings["username"].replace("@", "").lower()

    if username != admin_username:
        return

    # Check approve word
    if message.text.strip().upper() != settings["approve"].upper():
        return

    # Reply must be a deal form
    if "DEAL INFO" not in replied.text.upper():
        return

    await replied.reply(
        f"""<b>WALLET ADDRESS:</b>

<pre>{settings['wallet']}</pre>
""",
        parse_mode=ParseMode.HTML,
        quote=True
    )