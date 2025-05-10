from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import asyncio

# Initialize your bot
app = Client(
    "my_bot",
    bot_token="6757393088:AAFa9YEslZ5cKZecTnG0wf_txnRC3q_xj60",
    api_id=26847865,
    api_hash="0ef9fdd3e5f1ed49d4eb918a07b8e5d6"
)

@app.on_message(filters.private & filters.command("start"))
async def start_handler(client, message):
    if len(message.command) > 1:
        payload = message.command[1]
        new_link = f"https://t.me/DriveOO1bot?start={payload}"

        sent = await message.reply_text(
            "This message will be deleted in 10 minutes. Use link before that.",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Click here", url=new_link)]]
            )
        )
        await asyncio.sleep(600)
        await sent.delete()
    else:
        await message.reply_text("Welcome! Please use a valid start link.")

# Start the bot
app.run()