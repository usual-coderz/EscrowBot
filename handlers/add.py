from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from database import admins


@Client.on_message(filters.command("add") & filters.reply)
async def add_payment(client, message):
    settings = await admins.find_one({"chat_id": message.chat.id})

    if not settings:
        return

    username = (message.from_user.username or "").lower()
    admin_username = settings.get("username", "").replace("@", "").lower()

    if username != admin_username:
        return

    if len(message.command) != 2:
        return await message.reply(
            "Usage:\n/add <amount>",
            quote=True
        )

    try:
        amount = float(message.command[1])
    except (ValueError, TypeError):
        return await message.reply(
            "Invalid amount.",
            quote=True
        )

    if amount <= 0:
        return await message.reply(
            "Amount must be greater than 0.",
            quote=True
        )

    replied = message.reply_to_message

    if not replied or not replied.text:
        return await message.reply(
            "Please reply to a valid message.",
            quote=True
        )

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "1%",
                    callback_data=f"fee|1|{amount}|{replied.id}"
                ),
                InlineKeyboardButton(
                    "0.7%",
                    callback_data=f"fee|0.7|{amount}|{replied.id}"
                )
            ]
        ]
    )

    await message.reply(
        "<b>Select Escrow Fee:</b>",
        reply_markup=keyboard,
        quote=True
    )