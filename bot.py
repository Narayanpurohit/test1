session_string = "BAGZqnkAfBQpLUqWCLx93byHawqWJqKIlf4ONmmC6ZGcAD_40hfxCmhacQvehgaOJOU_RWwN2-ipKydjHrdwftMO1S_ezEQk-W155BB3FZnJZ6ztWXARuwgv444xopm-K9p1d6rAlClTX04dLmivzsMMEBeiUWn8WGWr_N5PMCzMrvcStj63ZygaZJhazlSxxHjX5NCWkeMFXtrMHOKa8UwTzVAInBMSk2Ud_yPhMnLNBzqc4Yrspt64MemA1IntuEBk08nBFw1OVXze0kaIHQTmugKt6l5po6LE0J1Rqfsm9SNy03NT6-wgWeIXOhhxCRmdnQEDSJJ0H8XOcTSK9k6kforRnwAAAAGUqifiAA"  
import asyncio
import os
from pyrogram import Client, errors, filters, idle

api_id = 26847865  
api_hash = "0ef9fdd3e5f1ed49d4eb918a07b8e5d6"  


group_id = -1002221607316  # Replace with your target group ID
forward_to = "me"  # Upload videos to Saved Messages

# Bot usernames to monitor
source_bots = ["Nagrufilesbot", "Fastvideoeditorbot"]

# Messages to send in order
messages = [
    "Ddart",
    "Ffootball",
    "Bbasket",
    "Sslot",
    "Bowling"
]

app = Client("my_userbot", api_id, api_hash, session_string=session_string)

async def send_messages():
    """ Sends scheduled messages to the group every 160 seconds """
    while True:
        for message in messages:
            try:
                await app.send_message(group_id, message)
                print(f"✅ Sent: {message}")
            except errors.FloodWait as e:
                print(f"⏳ FloodWait detected! Sleeping for {e.value} seconds...")
                await asyncio.sleep(e.value)
            except Exception as e:
                print(f"❌ Error sending message: {e}")

            await asyncio.sleep(160)  # Wait 160 seconds before sending the next message

@app.on_message(filters.chat(source_bots) & filters.video)
async def download_and_upload(client, message):
    """ Downloads the video from bot messages & re-uploads to Saved Messages """
    try:
        download_path = await message.download()
        print(f"📥 Downloaded video: {download_path}")

        # Upload to Saved Messages
        await app.send_video(forward_to, video=download_path, caption="Re-uploaded Video")
        print("📤 Uploaded video to Saved Messages.")

        # Remove the file after uploading
        os.remove(download_path)
        print("🗑️ Deleted downloaded video from VPS.")

    except errors.FloodWait as e:
        print(f"⏳ FloodWait while uploading! Sleeping for {e.value} seconds...")
        await asyncio.sleep(e.value)
    except Exception as e:
        print(f"❌ Error handling video: {e}")

async def main():
    print("🚀 Userbot started successfully!")

    # Start sending messages in the background
    asyncio.create_task(send_messages())

    # Keep the bot running
    await idle()

if __name__ == "__main__":
    app.run(main())  # ✅ Runs everything inside Pyrogram’s event loop (No conflicts)