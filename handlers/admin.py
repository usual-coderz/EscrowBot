from config import OWNER_ID

@Client.on_message(filters.command("setadmin"))
async def set_admin(client, message):

    if message.from_user.id != OWNER_ID:
        return await message.reply("You are not authorized to use this command.")

    if len(message.command) != 4:
        return await message.reply(
            "Usage:\n"
            "/setadmin <wallet_address> <approve_word> <@username>"
        )

    wallet = message.command[1].strip()
    approve = message.command[2].strip().upper()
    username = message.command[3].strip().lower()

    if not username.startswith("@"):
        username = "@" + username

    await admins.update_one(
        {"chat_id": message.chat.id},
        {
            "$set": {
                "chat_id": message.chat.id,
                "wallet": wallet,
                "approve": approve,
                "username": username
            }
        },
        upsert=True
    )

    await message.reply(
        f"""<b>Escrow Settings Saved</b>

<b>Admin:</b> {username}
<b>Approve Word:</b> <code>{approve}</code>

<b>Wallet Address:</b>
<pre>{wallet}</pre>
""",
        parse_mode="html"
    )