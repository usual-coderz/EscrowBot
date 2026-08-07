from pyrogram import Client

from config import *

app = Client(
    "escrow",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="handlers")
)

print("Bot Started")

app.run()