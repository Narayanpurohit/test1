
api_id = 26847865  
api_hash = "0ef9fdd3e5f1ed49d4eb918a07b8e5d6"  

group_id = -1002221607316  

import asyncio
from pyrogram import Client

# Replace with your actual credentials
api_id = 26847865  
api_hash = "0ef9fdd3e5f1ed49d4eb918a07b8e5d6"  
session_string = "BAGZqnkAfBQpLUqWCLx93byHawqWJqKIlf4ONmmC6ZGcAD_40hfxCmhacQvehgaOJOU_RWwN2-ipKydjHrdwftMO1S_ezEQk-W155BB3FZnJZ6ztWXARuwgv444xopm-K9p1d6rAlClTX04dLmivzsMMEBeiUWn8WGWr_N5PMCzMrvcStj63ZygaZJhazlSxxHjX5NCWkeMFXtrMHOKa8UwTzVAInBMSk2Ud_yPhMnLNBzqc4Yrspt64MemA1IntuEBk08nBFw1OVXze0kaIHQTmugKt6l5po6LE0J1Rqfsm9SNy03NT6-wgWeIXOhhxCRmdnQEDSJJ0H8XOcTSK9k6kforRnwAAAAGUqifiAA"  

group_id = -1002221607316  # Replace with your target group ID
message_text = "ddart"  
message_text2 = "ffootball"
message_text3 = "bbasket"
message_text4 = "sslot"


app = Client("my_userbot", api_id, api_hash, session_string=session_string)

async def send_message():
    while True:
        await app.send_message(group_id, message_text)
        print("Message sent!")
        await asyncio.sleep(120)  
        
        await app.send_message(group_id, message_text2)
        print("Message sent!")
        await asyncio.sleep(120)
        
        await app.send_message(group_id, message_text3)
        print("Message sent!")
        await asyncio.sleep(120)
        
        await app.send_message(group_id, message_text4)
        print("Message sent!")
        await asyncio.sleep(400)
        

async def main():
    async with app:
        await send_message()

if __name__ == "__main__":
    asyncio.run(main())