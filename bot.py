# bot.py

from pyrogram import Client, filters
from pyrogram.types import Message
from config import API_ID, API_HASH, BOT_TOKEN, ADMINS
from userbot import (
    is_logged_in,
    login_userbot,
    complete_login,
    logout_userbot,
    get_userbot_groups,
    broadcast_to_groups
)

pending_logins = {}

bot = Client("controller-bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

def is_admin(user_id):
    return user_id in ADMINS

@bot.on_message(filters.command("start"))
async def start(client, message: Message):
    if not is_admin(message.from_user.id):
        return await message.reply("❌ You're not allowed to use this bot.")
    await message.reply("🤖 Bot is ready. Use /login to start userbot session.")

# ------------------------- LOGIN -------------------------

@bot.on_message(filters.command("login"))
async def login(client, message: Message):
    if not is_admin(message.from_user.id):
        return await message.reply("❌ Unauthorized.")
    if is_logged_in():
        return await message.reply("✅ Already logged in.")
    await message.reply("📞 Please send your phone number in format +1234567890")
    pending_logins[message.from_user.id] = {"step": "phone"}

@bot.on_message(filters.command("logout"))
async def logout(client, message: Message):
    if not is_admin(message.from_user.id):
        return await message.reply("❌ Unauthorized.")
    if not is_logged_in():
        return await message.reply("⚠️ Userbot is not logged in.")
    msg = await message.reply("⏳ Logging out...")
    result = await logout_userbot()
    await msg.edit(result)

@bot.on_message(filters.text & filters.private)
async def handle_login_steps(client, message: Message):
    user_id = message.from_user.id
    if not is_admin(user_id):
        return

    if user_id not in pending_logins:
        return

    data = pending_logins[user_id]

    if data["step"] == "phone":
        data["phone"] = message.text
        response = await login_userbot(message.text)
        await message.reply(response)
        data["step"] = "code"

    elif data["step"] == "code":
        response = await complete_login(code=message.text)
        if "2FA" in response:
            await message.reply(response)
            data["step"] = "password"
        else:
            await message.reply(response)
            del pending_logins[user_id]

    elif data["step"] == "password":
        response = await complete_login(code=data.get("code"), password=message.text)
        await message.reply(response)
        del pending_logins[user_id]

# ----------------------- BROADCAST -----------------------

@bot.on_message(filters.command("broadcast") & filters.reply)
async def handle_broadcast(client: Client, message: Message):
    if not is_admin(message.from_user.id):
        return await message.reply("❌ Unauthorized.")

    if not is_logged_in():
        return await message.reply("⚠️ Userbot is not logged in. Use /login first.")

    reply_msg = message.reply_to_message
    status_msg = await message.reply("🔄 Fetching groups...")

    groups = await get_userbot_groups()
    if not groups:
        return await status_msg.edit("⚠️ No groups found.")

    await status_msg.edit(f"📢 Broadcasting to {len(groups)} groups...")

    stats = await broadcast_to_groups(reply_msg, groups)

    await status_msg.edit(
        f"✅ Broadcast Complete\n\n"
        f"✔️ Sent: {stats['success']}\n"
        f"❌ Failed: {stats['failed']}\n"
        f"📊 Total: {stats['total']} groups"
    )

bot.run()