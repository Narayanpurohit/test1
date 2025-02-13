import logging
from pyrogram import Client, filters
from pyrogram.types import Message
import requests

# Enable logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Replace these with your actual values
API_ID = 15191874 # Get from https://my.telegram.org
API_HASH = "3037d39233c6fad9b80d83bb8a339a07"  # Get from https://my.telegram.org
BOT_TOKEN = "6941908449:AAEYa6mME5Y90P9hb0zeu85yuF0if3s0YR8"  # Get from BotFather

# Initialize the Pyrogram Client
app = Client("terabox_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Start Command
@app.on_message(filters.command("start"))
async def start_command(client: Client, message: Message):
    await message.reply_text("Welcome! Send me a Terabox link, and I'll download the file for you.")

# Handle Terabox Links
@app.on_message(filters.text & filters.command)
async def handle_terabox_link(client: Client, message: Message):
    user_message = message.text
    if "terabox.com" in user_message:
        try:
            # Placeholder function to download the file from Terabox
            file_path = download_terabox_file(user_message)
            
            if file_path:
                await message.reply_text("Downloading your file...")
                await message.reply_document(document=file_path)
            else:
                await message.reply_text("Sorry, I couldn't download the file.")
        except Exception as e:
            logger.error(f"Error: {e}")
            await message.reply_text("An error occurred while processing your request.")
    else:
        await message.reply_text("Please send a valid Terabox link.")

# Placeholder function to download the file from Terabox
def download_terabox_file(url: str) -> str:
    try:
        # Replace this with your logic to download the file from Terabox
        # For example, using requests to download the file
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            file_name = "downloaded_file.mp4"  # Replace with the actual file name
            with open(file_name, "wb") as file:
                for chunk in response.iter_content(chunk_size=1024):
                    file.write(chunk)
            return file_name
        else:
            return None
    except Exception as e:
        logger.error(f"Error downloading file: {e}")
        return None

# Run the bot
if __name__ == "__main__":
    logger.info("Starting the bot...")
    app.run()