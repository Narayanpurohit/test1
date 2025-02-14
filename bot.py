import asyncio
from pyrogram import Client, errors


api_id = 26847865  
api_hash = "0ef9fdd3e5f1ed49d4eb918a07b8e5d6"  
session_string = "BAGZqnkAfBQpLUqWCLx93byHawqWJqKIlf4ONmmC6ZGcAD_40hfxCmhacQvehgaOJOU_RWwN2-ipKydjHrdwftMO1S_ezEQk-W155BB3FZnJZ6ztWXARuwgv444xopm-K9p1d6rAlClTX04dLmivzsMMEBeiUWn8WGWr_N5PMCzMrvcStj63ZygaZJhazlSxxHjX5NCWkeMFXtrMHOKa8UwTzVAInBMSk2Ud_yPhMnLNBzqc4Yrspt64MemA1IntuEBk08nBFw1OVXze0kaIHQTmugKt6l5po6LE0J1Rqfsm9SNy03NT6-wgWeIXOhhxCRmdnQEDSJJ0H8XOcTSK9k6kforRnwAAAAGUqifiAA"  

group_id = -1002221607316  # Replace with your target group ID


messages = [
    "Ddart",
    "Ffootball",
    "Bbasket",
    "Sslot",
    "bowling"
]

app = Client("my_userbot", api_id, api_hash, session_string=session_string)

async def send_messages():
    while True:
        for message in messages:
            try:
                await app.send_message(group_id, message)
                print(f"Sent: {message}")
            except errors.FloodWait as e:
                print(f"FloodWait detected! Sleeping for {e.value} seconds...")
                await asyncio.sleep(e.value)  # Wait for the required time
            except Exception as e:
                print(f"Error sending message: {e}")

            await asyncio.sleep(170)  # Wait 160 seconds before sending the next message

async def main():
    try:
        async with app:
            await send_messages()
    except Exception as e:
        print(f"Unexpected Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())