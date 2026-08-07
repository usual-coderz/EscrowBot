from pyrogram import Client, filters

# Sirf un users ke liye jo /dd use kar chuke hain
waiting = set()


@Client.on_message(filters.command("dd"))
async def new_deal(client, message):

    waiting.add(message.from_user.id)

    await message.reply(
        """Reply with:

DEAL INFO:
BUYER:
SELLER:
DEAL AMOUNT:
TIME TO COMPLETE DEAL:
""",
        quote=True
    )


@Client.on_message(filters.reply & filters.text)
async def deal_form(client, message):

    # Sirf wahi user jo /dd use kar chuka hai
    if message.from_user.id not in waiting:
        return

    replied = message.reply_to_message

    # Bot ke form ka hi reply hona chahiye
    if not replied or "Reply with:" not in replied.text:
        return

    waiting.remove(message.from_user.id)

    await message.reply(
        f"""✅ Deal Request Sent

{message.text}

⏳ Waiting For Escrow Admin Approval...
""",
        quote=True
    )