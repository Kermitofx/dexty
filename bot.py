import asyncio

from pyrogram import Client

from config import TOKEN, APP_ID, API_HASH, disabled_plugins, log_chat

with open("version.txt") as f:
    version = f.read().strip()


async def run_client(client):
    await client.start()
    await client.send_message(log_chat, "**Bot started**\n\n"
                                        f"**Version:** {version}")
    await client.idle()

client = Client("bot", bot_token=TOKEN, api_id=APP_ID, api_hash=API_HASH, plugins=dict(root="plugins", exclude=disabled_plugins))
client.run()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_client(client))
