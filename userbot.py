# userbot.py

from pyrogram import Client
from pyrogram.errors import FloodWait, SessionPasswordNeeded, PhoneCodeInvalid
from config import API_ID, API_HASH
import asyncio
import random
import os

session_file = "session.txt"
user_client = None
session_string = None


async def is_logged_in():
    return os.path.exists(session_file)


async def start_userbot():
    global session_string, user_client
    if not await is_logged_in():
        return False
    with open(session_file, "r") as f:
        session_string = f.read().strip()
    user_client = Client("dyn_session", api_id=API_ID, api_hash=API_HASH, session_string=session_string)
    await user_client.start()
    return True


async def login_start(phone: str):
    temp_client = Client("temp_login", api_id=API_ID, api_hash=API_HASH)
    await temp_client.connect()
    try:
        sent = await temp_client.send_code(phone)
        temp_client.phone = phone
        temp_client.phone_code_hash = sent.phone_code_hash
        return temp_client
    except Exception as e:
        await temp_client.disconnect()
        return f"❌ Failed to send code: {e}"


async def login_complete_code(client: Client, code: str):
    try:
        code = code.replace(" ", "")
        await client.sign_in(
            phone_number=client.phone,
            phone_code_hash=client.phone_code_hash,
            phone_code=code
        )
        return client
    except SessionPasswordNeeded:
        return "2FA"
    except PhoneCodeInvalid:
        return "❌ Invalid code. Please try again."
    except Exception as e:
        return f"❌ Login failed: {e}"


async def login_password(client: Client, password: str):
    try:
        await client.check_password(password=password)
        global session_string
        session_string = await client.export_session_string()
        with open(session_file, "w") as f:
            f.write(session_string)
        await client.disconnect()
        return "✅ Login successful. Session saved."
    except Exception as e:
        return f"❌ Password error: {e}"


async def logout_userbot():
    global session_string, user_client
    try:
        if user_client:
            await user_client.log_out()
            await user_client.stop()
        session_string = None
        user_client = None
        if os.path.exists(session_file):
            os.remove(session_file)
        return "✅ Logged out and session deleted."
    except Exception as e:
        return f"❌ Logout failed: {e}"


async def get_userbot_groups():
    groups = []
    async for dialog in user_client.get_dialogs():
        if dialog.chat.type in ["group", "supergroup"]:
            groups.append(dialog.chat.id)
    return groups


async def broadcast_to_groups(original_message, groups: list) -> dict:
    success, failed = 0, 0
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
        await asyncio.sleep(random.randint(10, 30))
    return {"success": success, "failed": failed, "total": len(groups)}