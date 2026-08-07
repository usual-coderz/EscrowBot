from pyrogram import Client, filters
from pyrogram.enums import ParseMode

FORM = """DEAL INFO :
BUYER :
SELLER :
TIME :
AMOUNT : $
CONDITIONS :
"""

waiting = set()


@Client.on_message(
    (filters.command("dd") | filters.regex(r"^(?i)dd$"))
    & filters.group
)
async def create_deal(client, message):

    waiting.add(message.from_user.id)

    await message.reply(
        f"<code>{FORM}</code>",
        parse_mode=ParseMode.HTML,
        quote=True
    )


@Client.on_message(filters.reply & filters.text)
async def receive_form(client, message):

    if message.from_user.id not in waiting:
        return

    if not message.reply_to_message:
        return

    waiting.remove(message.from_user.id)

    await message.reply(
        f"<code>{message.text}</code>",
        parse_mode=ParseMode.HTML,
        quote=True
    )