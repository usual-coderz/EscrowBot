from pyrogram import Client, filters

waiting = {}

@Client.on_message(filters.command("dd"))
async def new_deal(client, message):

    waiting[message.from_user.id] = True

    await message.reply(
"""Reply with:

DEAL INFO:
BUYER:
SELLER:
DEAL AMOUNT:
TIME TO COMPLETE DEAL:
"""
    )


@Client.on_message(filters.reply)
async def form(client, message):

    if message.from_user.id not in waiting:
        return

    waiting.pop(message.from_user.id)

    text = message.text

    await message.reply(
f"""✅ Deal Request Sent

{text}

Waiting For Escrow Admin Approval...
"""
    )