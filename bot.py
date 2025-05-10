from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import UserNotParticipant, PeerIdInvalid, ChatAdminRequired
from pyrogram.enums import ChatMemberStatus
import asyncio

API_ID = 26847865
API_HASH = "0ef9fdd3e5f1ed49d4eb918a07b8e5d6"
BOT_TOKEN = "6757393088:AAFa9YEslZ5cKZecTnG0wf_txnRC3q_xj60"

# Channel info
REQUIRED_CHANNEL_ID = -1002649752447  # Replace with your channel's ID
REDIRECT_BOT = "DriveOO1bot"

app = Client("redirect_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.private & filters.command("start"))
async def start_handler(client, message):
    user_id = message.from_user.id
    payload = message.command[1] if len(message.command) > 1 else None

    if not payload:
        await message.reply_text("Welcome! Please use a valid start link.")
        return

    print(f"User {user_id} started bot with payload: {payload}")

    # Check if user is in the required channel
    try:
        member = await client.get_chat_member(REQUIRED_CHANNEL_ID, user_id)
        print(f"[DEBUG] User {user_id} status in channel: {member.status}")

        if member.status not in (
            ChatMemberStatus.MEMBER,
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.OWNER
        ):
            print(f"[DEBUG] User {user_id} is NOT a valid member")
            raise UserNotParticipant

    except UserNotParticipant:
        print(f"[DEBUG] UserNotParticipant triggered for user {user_id}")
        invite = await app.create_chat_invite_link(REQUIRED_CHANNEL_ID)
        invite_link = invite.invite_link
        try_again_link = f"https://t.me/{client.me.username}?start={payload}"

        await message.reply_text(
            "You have to join this channel to use this bot.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Join Channel", url=invite_link)],
                [InlineKeyboardButton("Try Again", url=try_again_link)]
            ])
        )
        return
    except ChatAdminRequired:
        print(f"[ERROR] Bot is not admin in the channel!")
        await message.reply_text("Error: Bot must be admin in the channel to check membership.")
        return
    except PeerIdInvalid:
        print(f"[ERROR] Invalid channel ID: {REQUIRED_CHANNEL_ID}")
        await message.reply_text("Error: Invalid channel configuration.")
        return
    except Exception as e:
        print(f"[ERROR] Unexpected error while checking membership: {e}")
        await message.reply_text("Something went wrong while checking your join status.")
        return

    # User is in channel, send redirect link
    target_link = f"https://t.me/{REDIRECT_BOT}?start={payload}"
    sent = await message.reply_text(
        "This message will be deleted in 10 minutes. Use the link before that.",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("Click here", url=target_link)]]
        )
    )

    await asyncio.sleep(600)
    await sent.delete()

app.run()