# bot.py

from pyrogram import Client, filters
from pyrogram.types import Message
from config import API_ID, API_HASH, BOT_TOKEN, ADMINS
import userbot

bot = Client("controller-bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

login_sessions = {}

def is_admin(user_id):
    return user_id in ADMINS
@bot.on_message(filters.command("groups"))
async def list_groups(client, message: Message):
    if not is_admin(message.from_user.id):
        return

    if not await userbot.is_logged_in():
        return await message.reply("⚠️ Please login first using /login.")

    await userbot.start_userbot()
    groups = await userbot.get_userbot_groups()
    
    if not groups:
        return await message.reply("❌ No groups found.")

    msg = "**📋 Groups Joined:**\n"
    for i, group_id in enumerate(groups, 1):
        try:
            chat = await userbot.user_client.get_chat(group_id)
            msg += f"{i}. {chat.title} (`{group_id}`)\n"
        except:
            msg += f"{i}. [Failed to fetch name] (`{group_id}`)\n"

    # Telegram limits messages to 4096 characters
    if len(msg) > 4000:
        with open("groups.txt", "w", encoding="utf-8") as f:
            f.write(msg)
        await message.reply_document("groups.txt", caption)

@bot.on_message(filters.command("start"))
async def start(client, message: Message):
    if not is_admin(message.from_user.id):
        return await message.reply("❌ You're not authorized.")
    await message.reply("🤖 Bot is online.\nUse /login to log in and /help for commands.")

@bot.on_message(filters.command("help"))
async def help_command(client, message: Message):
    if not is_admin(message.from_user.id):
        return
    await message.reply(
        "**🤖 Available Commands:**\n"
        "/login - Start userbot login\n"
        "/logout - Logout and delete session\n"
        "/broadcast - Reply to a message to broadcast\n"
        "/help - Show this help message"
    )

@bot.on_message(filters.command("login"))
async def login(client, message: Message):
    if not is_admin(message.from_user.id):
        return await message.reply("❌ You're not authorized.")
    await message.reply("📞 Send your phone number in international format (e.g., `+1234567890`)")
    login_sessions[message.from_user.id] = {"step": "phone"}

@bot.on_message(filters.command("logout"))
async def logout(client, message: Message):
    if not is_admin(message.from_user.id):
        return await message.reply("❌ You're not authorized.")
    if not await userbot.is_logged_in():
        return await message.reply("⚠️ Not logged in.")
    msg = await message.reply("⏳ Logging out...")
    result = await userbot.logout_userbot()
    await msg.edit(result)

@bot.on_message(filters.command("broadcast") & filters.reply)
async def broadcast(client, message: Message):
    if not is_admin(message.from_user.id):
        return
    if not await userbot.is_logged_in():
        return await message.reply("⚠️ Please login first using /login.")

    await userbot.start_userbot()

    status = await message.reply("🔍 Fetching groups...")
    groups = await userbot.get_userbot_groups()
    if not groups:
        return await status.edit("❌ No groups found.")

    await status.edit(f"📢 Broadcasting to {len(groups)} groups...")

    stats = await userbot.broadcast_to_groups(message.reply_to_message, groups)

    await status.edit(
        f"✅ Broadcast Complete\n\n"
        f"✔️ Sent: {stats['success']}\n"
        f"❌ Failed: {stats['failed']}\n"
        f"📊 Total: {stats['total']} groups"
    )

@bot.on_message(filters.private & filters.text)
async def handle_login_steps(client, message: Message):
    user_id = message.from_user.id
    if not is_admin(user_id):
        return

    if user_id not in login_sessions:
        return

    step_data = login_sessions[user_id]
    step = step_data["step"]

    if step == "phone":
        phone = message.text.strip()
        result = await userbot.login_start(phone)
        if isinstance(result, str):
            await message.reply(result)
            del login_sessions[user_id]
        else:
            step_data["client"] = result
            step_data["step"] = "code"
            await message.reply("📨 Now send the OTP (with spaces between digits). Example:\n`1 2 3 4 5`")

    elif step == "code":
        code = message.text.strip()
        result = await userbot.login_complete_code(step_data["client"], code)
        if isinstance(result, str):
            if result == "2FA":
                step_data["step"] = "password"
                await message.reply("🔐 Please send your 2FA password.")
            else:
                await message.reply(result)
                del login_sessions[user_id]
        else:
            userbot.session_string = await result.export_session_string()
            with open("session.txt", "w") as f:
                f.write(userbot.session_string)
            await result.disconnect()
            await message.reply("✅ Logged in successfully.")
            del login_sessions[user_id]

    elif step == "password":
        password = message.text.strip()
        result = await userbot.login_password(step_data["client"], password)
        await message.reply(result)
        del login_sessions[user_id]

bot.run()