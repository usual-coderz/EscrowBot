from pyrogram import Client, filters
from pyrogram.types import ChatJoinRequest
from database import settings

WELCOME = """Hey 👋

You've requested to join the official CRYPTO ESCROW GROUP 💎

Please remember:

• Verify the escrow admin's username before making any payment.

• Re-verify the escrow group from the official main group.

• Never rush. Observe the escrow activity first. If you find anything suspicious, report it immediately.

Stay safe and enjoy secure trading.
"""


@Client.on_message(filters.command("autoapprove"))
async def autoapprove(client, message):

    member = await client.get_chat_member(
        message.chat.id,
        message.from_user.id
    )

    if member.status not in ("administrator", "owner"):
        return await message.reply(
            "Only group admins can use this command."
        )

    if len(message.command) != 2:
        return await message.reply(
            "Usage:\n"
            "/autoapprove on\n"
            "/autoapprove off"
        )

    mode = message.command[1].lower()

    if mode not in ["on", "off"]:
        return await message.reply(
            "Use: on/off"
        )

    enabled = mode == "on"

    await settings.update_one(
        {"chat_id": message.chat.id},
        {
            "$set": {
                "chat_id": message.chat.id,
                "autoapprove": enabled
            }
        },
        upsert=True
    )

    await message.reply(
        f"Auto Approve {'Enabled' if enabled else 'Disabled'}."
    )


@Client.on_chat_join_request()
async def auto_accept(client, join_request: ChatJoinRequest):

    config = await settings.find_one(
        {"chat_id": join_request.chat.id}
    )

    if not config or not config.get("autoapprove", False):
        return

    try:
        await join_request.approve()

        try:
            await client.send_message(
                join_request.from_user.id,
                WELCOME
            )
        except Exception:
            pass

    except Exception as e:
        print(e)