

#API_ID = 15191874 # Get from https://my.telegram.org
API_HASH = "3037d39233c6fad9b80d83bb8a339a07"  # Get from https://my.telegram.org
BOT_TOKEN = "6941908449:AAEYa6mME5Y90P9hb0zeu85yuF0if3s0YR8"  
import asyncio
from pyrogram import Client

# Use session string instead of a filename
api_id = 15191874  # Replace with your API ID
api_hash = "3037d39233c6fad9b80d83bb8a339a07"  # Replace with your API Hash
session_string = "BQDnz0IAbrET1b89Vlg4OYD7UScdllLaVMO64LMokSL8ux2FRwYdOhdTvw-LxHoZ1XNZ3s5T8sX-IxZcvxSxrsvLYHjPx1imajxvKVcixAd4_OXsOExJ9vgfh3T3-y6MMbrq6jnhNEbqfJxNIZxj5N5hFQbtGrwNnHElr7kcOM-yJfm_90xrLhVrW9ILvCBs9MA5taV5EJ9uFX4usuEfyalQ4FMGnnb-IGUiXlHeY3xjw3tVww690U5mOPTHCnKxrjMTSic3QkthgJMeFS_VzwlON9Xts4wvxCni78QElDsCeB0Va0FVoo1gJawGcBs8ng1cPWIYEQ_akySd6tz-TVJlGu-DcgAAAAFNo2ggAA"  # Replace with your actual session string

group_id = -1001234567890  # Replace with your target group ID
message_text = "This is an automated message!"  # Customize your message

app = Client("my_userbot", api_id, api_hash, session_string=session_string)

async def send_message():
    while True:
        async with app:
            await app.send_message(group_id, message_text)
            print("Message sent!")
        await asyncio.sleep(300)  # Wait for 5 minutes (300 seconds)

if __name__ == "__main__":
    asyncio.run(send_message())