

API_ID = 15191874 # Get from https://my.telegram.org
API_HASH = "3037d39233c6fad9b80d83bb8a339a07"  # Get from https://my.telegram.org
BOT_TOKEN = "6941908449:AAEYa6mME5Y90P9hb0zeu85yuF0if3s0YR8"  
import logging
import os
import aiohttp
from pyrogram import Client, filters
from pyrogram.types import Message
from urllib.parse import urlparse


# Enable logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Initialize Pyrogram Client
app = Client("terabox_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Directory to save downloads
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Start Command
@app.on_message(filters.command("start"))
async def start_command(client: Client, message: Message):
    await message.reply_text("Welcome! Send me a Terabox link, and I'll download the file for you.")

# Handle Terabox Links
@app.on_message(filters.text & ~filters.command)
async def handle_terabox_link(client: Client, message: Message):
    user_message = message.text.strip()

    if "terabox.com" in user_message:
        try:
            status_msg = await message.reply_text("🔄 Processing your Terabox link...")

            # Download the file
            file_path = await download_terabox_file(user_message)

            if file_path:
                await status_msg.edit_text("📤 Uploading your file...")
                await message.reply_document(document=file_path)

                # Clean up after sending
                os.remove(file_path)
            else:
                await status_msg.edit_text("❌ Failed to download the file. The link might be invalid or expired.")
        
        except Exception as e:
            logger.error(f"Error: {e}")
            await message.reply_text("⚠️ An error occurred while processing your request. Please try again.")
    else:
        await message.reply_text("⚠️ Please send a valid Terabox link.")

# Asynchronous function to download the file from Terabox
async def download_terabox_file(url: str) -> str:
    """Downloads a file from the given Terabox URL and saves it locally."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    # Extract file name from URL or assign default name
                    parsed_url = urlparse(url)
                    filename = os.path.basename(parsed_url.path) or "downloaded_file"

                    file_path = os.path.join(DOWNLOAD_DIR, filename)

                    # Save the file asynchronously
                    with open(file_path, "wb") as file:
                        async for chunk in response.content.iter_chunked(1024):
                            file.write(chunk)

                    return file_path
                else:
                    logger.error(f"Failed to download file, status code: {response.status}")
                    return None
    except Exception as e:
        logger.error(f"Error downloading file: {e}")
        return None

# Run the bot
if __name__ == "__main__":
    logger.info("✅ Bot is starting...")
    app.run()