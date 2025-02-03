from pyrogram import Client, filters
import os

# Your API credentials
API_ID = 20672791  # Replace with your API ID
API_HASH = "4ad574250a28647258b597c01cbd8028"  # Replace with your API Hash
SAVE_CHAT_ID = "me"  # Change to your private channel ID if needed

# Start the Userbot
app = Client("userbot", api_id=API_ID, api_hash=API_HASH)

# Function to save restricted content
@app.on_message(filters.bot & filters.media)
def save_restricted(client, message):
    # Create a downloads folder if not exists
    if not os.path.exists("downloads"):
        os.makedirs("downloads")

    # Download media
    file_path = message.download(file_name=f"downloads/{message.id}")
    print(f"Downloaded: {file_path}")

    # Send to Saved Messages or Private Channel
    client.send_document(SAVE_CHAT_ID, file_path, caption="Saved from restricted bot")

@app.on_message(filters.bot & filters.text)
def save_text(client, message):
    client.send_message(SAVE_CHAT_ID, f"📩 **Restricted Message Saved:**\n\n{message.text}")

print("Userbot is running...")
app.run()