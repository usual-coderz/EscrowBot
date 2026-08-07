from pyrogram import Client, filters
from database import admins


@Client.on_message(filters.reply & filters.text)
async def approve_deal(client, message):

    # Get escrow settings for this group
    settings = await admins.find_one({"chat_id": message.chat.id})

    if not settings:
        return

    # Must be a reply
    if not message.reply_to_message:
        return

    # Only configured admin can approve
    if (message.from_user.username or "").lower() != settings["username"].replace("@", "").lower():
        return

    # Check approve word
    if message.text.strip().upper() != settings["approve"].strip().upper():
        return

    # Reply must contain the deal form
    if not message.reply_to_message.text:
        return

    if "DEAL INFO" not in message.reply_to_message.text.upper():
        return

    # Send only wallet address
    await message.reply(
        f"""<b>WALLET ADDRESS:</b>

<pre>{settings['wallet']}</pre>
""",
        parse_mode="html",
        quote=True
    )