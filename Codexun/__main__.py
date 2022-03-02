import asyncio
import requests
from pyrogram import Client
from pytgcalls import idle
from Codexun import app
from driver.veez import call_py, bot
from Codexun.database.functions import clean_restart_stage
from Codexun.database.queue import get_active_chats, remove_active_chat
from Codexun.tgcalls.calls import run
from Codexun.config import API_ID, API_HASH, BOT_TOKEN, BG_IMG


response = requests.get(BG_IMG)
with open("./etc/foreground.png", "wb") as file:
    file.write(response.content)


async def load_start():
    restart_data = await clean_restart_stage()
    if restart_data:
        print("[INFO]: SENDING RESTART STATUS")
        try:
            await app.edit_message_text(
                restart_data["chat_id"],
                restart_data["message_id"],
                "**Restarted the Bot Successfully.**",
            )
        except Exception:
            pass
    served_chats = []
    try:
        chats = await get_active_chats()
        for chat in chats:
            served_chats.append(int(chat["chat_id"]))
    except Exception as e:
        print("Error came while clearing db")
    for served_chat in served_chats:
        try:
            await remove_active_chat(served_chat)
        except Exception as e:
            print("Error came while clearing db")
            pass
    print("[INFO]: STARTED")
    await call_py.start()
    print("[INFO]: PYTGCALLS CLIENT STARTED !!")


loop = asyncio.get_event_loop_policy().get_event_loop()
loop.run_until_complete(load_start())

Client(
    ":memory:",
    API_ID,
    API_HASH,
    bot_token=BOT_TOKEN,
    plugins={"root": "Codexun.modules"},
).start()

run()
idle()
loop.close()
