from pyrogram import Client, filters
from database import admins
import random
import string


def trade_id():
    return "#TID" + "".join(random.choices(string.ascii_uppercase + string.digits, k=6))


@Client.on_message(filters.reply & filters.text)
async def approve_deal(client, message):

    # Admin ki settings
    admin = await admins.find_one({"chat_id": message.chat.id})
    if not admin:
        return

    # Reply message hona chahiye
    if not message.reply_to_message:
        return

    replied = message.reply_to_message

    # Sirf configured admin
    if message.from_user.username != admin["username"].replace("@", ""):
        return

    # Sirf approve word
    if message.text.strip().upper() != admin["approve"].strip().upper():
        return

    # Deal form verify
    if "DEAL INFO:" not in replied.text:
        return

    buyer = ""
    seller = ""
    amount = ""
    deal_info = ""
    time = ""

    for line in replied.text.splitlines():

        line = line.strip()

        if line.startswith("DEAL INFO:"):
            deal_info = line.replace("DEAL INFO:", "").strip()

        elif line.startswith("BUYER:"):
            buyer = line.replace("BUYER:", "").strip()

        elif line.startswith("SELLER:"):
            seller = line.replace("SELLER:", "").strip()

        elif line.startswith("DEAL AMOUNT:"):
            amount = line.replace("DEAL AMOUNT:", "").strip()

        elif line.startswith("TIME TO COMPLETE DEAL:"):
            time = line.replace("TIME TO COMPLETE DEAL:", "").strip()

    await replied.reply(
f"""🛡 ESCROW APPROVED

💰 Payment Address
`{admin['wallet']}`

📦 Deal Info: {deal_info}

💵 Amount: {amount}

⏳ Time: {time}

🆔 Trade ID: {trade_id()}

👤 Buyer: {buyer}
👤 Seller: {seller}

Please send the payment to the address above.
"""
    )