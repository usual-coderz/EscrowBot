from pyrogram import Client, filters
from database import admins
import random
import string


def trade_id():
    return "#TID" + "".join(random.choices(string.ascii_uppercase, k=6))


@Client.on_message(filters.reply & filters.text)
async def approve_deal(client, message):

    replied = message.reply_to_message

    if not replied or not replied.text:
        return

    admin = await admins.find_one({"chat_id": message.chat.id})
    if not admin:
        return

    # Sirf configured admin approve kar sakta hai
    if message.from_user.username != admin["username"].replace("@", ""):
        return

    # Sirf configured approve word
    if message.text.strip() != admin["approve"]:
        return

    # Reply kiya gaya message deal form hona chahiye
    if "DEAL INFO:" not in replied.text:
        return

    lines = replied.text.splitlines()

    buyer = lines[1].replace("BUYER:", "").strip()
    seller = lines[2].replace("SELLER:", "").strip()
    amount = lines[3].replace("DEAL AMOUNT:", "").strip()

    await replied.reply(
        f"""🛡 ESCROW APPROVED

💰 Payment Address:
`{admin['wallet']}`

💵 Amount:
{amount}

🆔 Trade ID:
{trade_id()}

Buyer: {buyer}
Seller: {seller}

Please send the payment to the address above."""
    )