# userbot.py

from pyrogram import Client
from pyrogram.errors import FloodWait, SessionPasswordNeeded
from config import API_ID, API_HASH
import asyncio
import random
import os

SESSION_FILE = "userbot"

user = Client(SESSION_FILE, api_id=API_ID, api_hash=API_HASH)

def is_logged_in() -> bool:
    return os.path.exists(f"{SESSION_FILE}.session")

async def login_userbot(phone_number: str) -> str:
    await user.connect()
    try:
        sent_code = await user.send_code(phone_number)
        return "📲 Please enter the code sent to your Telegram account."
    except Exception as e:
        return f"❌ Failed to send code: {e}"

async def complete_login(code: str, password: str = None) -> str:
    try:
        if password:
            await user.sign_in(code=code, password=password)
        else:
            await user.sign_in(code=code)
        return "✅ Logged in successfully."
    except SessionPasswordNeeded:
        return "🔐 2FA is enabled. Please send your password."
    except Exception as e:
        return f"❌ Login failed: {e}"
    finally:
        await user.disconnect()

async def logout_userbot() -> str:
    try:
        await user.start()
        await user.log_out()
        await user.stop()
        os.remove(f"{SESSION_FILE}.session")
        return "✅ Userbot logged out and session cleared."
    except Exception as e:
        return f"❌ Logout failed: {e}"

async def get_userbot_groups() -> list:
    groups = []
    async with user:
        async for dialog in user.get_dialogs():
            if dialog.chat.type in ["group", "supergroup"]:
                groups.append(dialog.chat.id)
    return groups

async def broadcast_to_groups(original_message, groups: list) -> dict:
    success, failed = 0, 0
    async with user:
        for chat_id in groups:
            try:
                await original_message.copy(chat_id)
                success += 1
            except FloodWait as e:
                await asyncio.sleep(e.value)
                try:
                    await original_message.copy(chat_id)
                    success += 1
                except Exception:
                    failed += 1
            except Exception:
                failed += 1

            await asyncio.sleep(random.uniform(10, 30))
    return {"success": success, "failed": failed, "total": len(groups)}