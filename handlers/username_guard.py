from pyrogram import Client, filters
from pyrogram.enums import ChatMemberStatus

from database import warnings


MAX_WARNS = 3


@Client.on_message(filters.group & ~filters.service)
async def username_guard(client, message):

    user = message.from_user

    if not user:
        return

    # Ignore bots
    if user.is_bot:
        return

    # Ignore admins & owners
    try:
        member = await client.get_chat_member(
            message.chat.id,
            user.id
        )

        if member.status in [
            ChatMemberStatus.OWNER,
            ChatMemberStatus.ADMINISTRATOR
        ]:
            return

    except:
        return

    # User has username
    if user.username:

        await warnings.delete_one(
            {
                "chat_id": message.chat.id,
                "user_id": user.id
            }
        )

        return

    # Increase warning
    data = await warnings.find_one(
        {
            "chat_id": message.chat.id,
            "user_id": user.id
        }
    )

    count = 1

    if data:
        count = data["count"] + 1

    await warnings.update_one(
        {
            "chat_id": message.chat.id,
            "user_id": user.id
        },
        {
            "$set": {
                "username": user.first_name,
                "count": count
            }
        },
        upsert=True
    )

    # Ban after 3 warnings
    if count >= MAX_WARNS:

        try:
            await client.ban_chat_member(
                message.chat.id,
                user.id
            )

            await message.reply(
                f"""🚫 User Banned

Reason:
No Telegram username.

Warnings:
3/3
"""
            )

        except Exception:
            pass

        await warnings.delete_one(
            {
                "chat_id": message.chat.id,
                "user_id": user.id
            }
        )

        return

    # Warning
    await message.reply(
        f"""⚠️ Warning {count}/3

{user.mention}

You don't have a Telegram username.

Please set a username (@username).

After 3 warnings you'll be removed automatically.
"""
    )