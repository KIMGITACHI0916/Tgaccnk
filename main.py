from telethon import TelegramClient, events
import asyncio
import os

api_id = int(os.getenv("TG_API_ID"))
api_hash = os.getenv("TG_API_HASH")
phone = os.getenv("TG_PHONE")
target = os.getenv("TG_TARGET")  # username or chat ID
message = os.getenv("TG_MESSAGE", "Hello! This message is sent every 5 seconds.")
interval = int(os.getenv("TG_INTERVAL", "5"))

client = TelegramClient("user_session", api_id, api_hash)

stop_flag = False  # will become True if the person replies


async def check_reply(event):
    global stop_flag
    # Only react if message is from the target chat and not from you
    sender = await event.get_sender()
    me = await client.get_me()
    if sender.id != me.id:
        chat = await event.get_chat()
        if str(chat.id) == str((await client.get_entity(target)).id):
            print(f"Received reply from {target}: {event.message.message}")
            stop_flag = True


async def main():
    global stop_flag
    await client.start(phone=phone)
    me = await client.get_me()
    print(f"Logged in as {me.first_name}")

    # Listen for incoming messages from the target
    client.add_event_handler(check_reply, events.NewMessage(from_users=None))

    try:
        entity = await client.get_entity(target)
        print(f"Target found: {entity.id}")

        while not stop_flag:
            await client.send_message(entity, message)
            print(f"Sent: {message}")
            await asyncio.sleep(interval)

        print("Stopped sending — target replied.")
    except KeyboardInterrupt:
        print("Stopped manually.")
    finally:
        await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
    
