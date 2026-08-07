from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from database import admins


@Client.on_message(filters.command("add") & filters.reply)
async def add_payment(client, message):

    settings = await admins.find_one({"chat_id": message.chat.id})

    if not settings:
        return

    # Only configured escrow admin
    if (message.from_user.username or "").lower() != settings["username"].replace("@", "").lower():
        return

    if len(message.command) != 2:
        return await message.reply("Usage:\n/add <amount>")

    try:
        amount = float(message.command[1])
    except ValueError:
        return await message.reply("Invalid amount.")

    replied = message.reply_to_message

    if not replied or not replied.text:
        return

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
        "Select Escrow Fee:",
        reply_markup=keyboard,
        quote=True
    )