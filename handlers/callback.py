from pyrogram import Client, filters
from pyrogram.types import CallbackQuery
from pyrogram.enums import ParseMode

from database import admins, trades

import random
import string


def generate_trade_id():
    return "#TID" + "".join(
        random.choices(
            string.ascii_uppercase + string.digits,
            k=6
        )
    )


@Client.on_callback_query(filters.regex(r"^fee\|"))
async def fee_callback(client, callback_query: CallbackQuery):

    data = callback_query.data.split("|")

    if len(data) != 4:
        return await callback_query.answer(
            "Invalid data",
            show_alert=True
        )

    fee_percent = float(data[1])
    amount = float(data[2])
    message_id = int(data[3])

    chat_id = callback_query.message.chat.id

    settings = await admins.find_one(
        {"chat_id": chat_id}
    )

    if not settings:
        return await callback_query.answer(
            "Escrow settings missing",
            show_alert=True
        )

    # Only escrow admin
    username = (
        callback_query.from_user.username or ""
    ).lower()

    admin_username = (
        settings["username"]
        .replace("@", "")
        .lower()
    )

    if username != admin_username:
        return await callback_query.answer(
            "Not authorized",
            show_alert=True
        )


    try:
        deal_message = await client.get_messages(
            chat_id,
            message_id
        )

    except Exception:
        return await callback_query.answer(
            "Deal message not found",
            show_alert=True
        )


    if not deal_message.text:
        return


    deal = {}

    for line in deal_message.text.splitlines():

        if ":" in line:
            key, value = line.split(":", 1)
            deal[key.strip().upper()] = value.strip()


    fee_amount = amount * fee_percent / 100

    release_amount = amount - fee_amount

    trade_id = generate_trade_id()


    # Save trade
    await trades.insert_one(
        {
            "trade_id": trade_id,
            "chat_id": chat_id,
            "amount": amount,
            "fee_percent": fee_percent,
            "fee_amount": fee_amount,
            "release_amount": release_amount,
            "buyer": deal.get("BUYER", "-"),
            "seller": deal.get("SELLER", "-"),
            "escrow_admin": settings["username"],
            "status": "ACTIVE"
        }
    )


    await deal_message.reply(
        f"""💰 Deal Amount: ${amount:.2f}
📥 Received Amount: ${amount:.2f}
📤 Release/Refund Amount: ${release_amount:.2f}
🆔 Trade ID: {trade_id}

Continue the Deal

Buyer: {deal.get("BUYER","-")}
Seller: {deal.get("SELLER","-")}

🛡 Escrowed By: {settings["username"]}
""",
        parse_mode=ParseMode.HTML
    )


    await callback_query.answer(
        f"{fee_percent}% Fee Applied"
    )