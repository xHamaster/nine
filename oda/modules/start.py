import asyncio

from pyrogram import Client, filters, __version__ as pyrover
from pyrogram.errors import FloodWait
from pytgcalls import (__version__ as pytover)
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, ChatJoinRequest
from oda.utils.filters import command

from oda.config import BOT_USERNAME


@Client.on_message(command("start") & filters.private & ~filters.edited)
async def start_(client: Client, message: Message):
    await message.reply_photo(
        photo=f"https://telegra.ph/file/e594d98181c2f54b872fd.jpg",
        caption=f"""**Welcome {message.from_user.mention()}** 👋

This is the resso music bot, a bot for playing high quality and unbreakable music in your groups voice chat.

Just add me to your group and make a admin with needed admin permission to perform a right actions !

Use the given buttons for more 📍""",
    reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Commands", callback_data="cbcmnds"),
                    InlineKeyboardButton(
                        "Commands", callback_data="cbabout")
                ],
                [
                    InlineKeyboardButton(
                        "Commands", callback_data="cbguide")
                ]
                
           ]
        ),
    )
