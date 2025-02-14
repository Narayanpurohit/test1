

#API_ID = 15191874 # Get from https://my.telegram.org
#API_HASH = "3037d39233c6fad9b80d83bb8a339a07"  # Get from https://my.telegram.org
#BOT_TOKEN = "6941908449:
api_id = 26847865  # Replace with your API ID
api_hash = "0ef9fdd3e5f1ed49d4eb918a07b8e5d6"  # Replace with your API Hash
 # Replace with your actual session string

group_id = -1002315666631  # Replace with your target group ID
import asyncio
from pyrogram import Client

# Replace with your actual credentials
api_id = 26847865  # Replace with your API ID
api_hash = "0ef9fdd3e5f1ed49d4eb918a07b8e5d6"  # Replace with your API Hash
session_string = "BQDnz0IAbrET1b89Vlg4OYD7UScdllLaVMO64LMokSL8ux2FRwYdOhdTvw-LxHoZ1XNZ3s5T8sX-IxZcvxSxrsvLYHjPx1imajxvKVcixAd4_OXsOExJ9vgfh3T3-y6MMbrq6jnhNEbqfJxNIZxj5N5hFQbtGrwNnHElr7kcOM-yJfm_90xrLhVrW9ILvCBs9MA5taV5EJ9uFX4usuEfyalQ4FMGnnb-IGUiXlHeY3xjw3tVww690U5mOPTHCnKxrjMTSic3QkthgJMeFS_VzwlON9Xts4wvxCni78QElDsCeB0Va0FVoo1gJawGcBs8ng1cPWIYEQ_akySd6tz-TVJlGu-DcgAAAAFNo2ggAA"  # Replace with your actual session string

group_id = -1002315666631
msg1 = "sslot"  
msg3 = "bbasket" 
msg2 = "ddart" 
msg4 = "ffootball" 
msg1 = "sslot" 

app = Client("my_userbot", api_id, api_hash, session_string=session_string)

async def send_message():
    while True:
        await app.send_message(group_id, msg5)
        print("Message sent!")
        await asyncio.sleep(300)
        await app.send_message(group_id, msg1)
        print("Message sent!")
        await asyncio.sleep(300)  
        await app.send_message(group_id, msg2)
        print("Message sent!")
        await asyncio.sleep(300)
        await app.send_message(group_id, msg3)
        print("Message sent!")
        await asyncio.sleep(300)
        await app.send_message(group_id, msg4)
        print("Message sent!")
        await asyncio.sleep(500)
        
        
        
        
        
async def main():
    async with app:
        await send_message()

if __name__ == "__main__":
    asyncio.run(main())