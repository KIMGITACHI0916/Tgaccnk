from telethon import TelegramClient
import asyncio
import os

api_id = int(os.getenv("TG_API_ID"))
api_hash = os.getenv("TG_API_HASH")
phone = os.getenv("TG_PHONE")
target = os.getenv("TG_TARGET")  # username or chat ID
message = os.getenv("TG_MESSAGE", "Hello! This message is sent every 5 seconds.")
interval = int(os.getenv("TG_INTERVAL", "5"))

client = TelegramClient("user_session", api_id, api_hash)

async def main():
    await client.start(phone=phone)
    user = await client.get_me()
    print(f"Logged in as {user.first_name}")

    try:
        while True:
            await client.send_message(target, message)
            print(f"Sent: {message}")
            await asyncio.sleep(interval)
    except KeyboardInterrupt:
        print("Stopped by user.")
    finally:
        await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
