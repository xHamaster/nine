
import asyncio

from pyrogram import Client, filters, __version__ as pyrover
from pyrogram.errors import FloodWait
from pytgcalls import (__version__ as pytover)
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, ChatJoinRequest


from oda.config import BOT_USERNAME

@Client.on_message(
    command(["start", f"start@{BOT_USERNAME}"]) & filters.private & ~filters.edited
)
async def start_(c: Client, message: Message):
    await message.reply_text(
        f"""💖 **Welcome {message.from_user.mention()}""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "➕ Add me to your Group ➕",
                        url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
                    )
                ],
                [InlineKeyboardButton("About", callback_data="user_guide")],
                [
                    InlineKeyboardButton("Commands", callback_data="command_list"),
                ],
                [
                    InlineKeyboardButton(
                        "Official Group", url=f"https://t.me/CreatorPavanChat"
                    ),
                    InlineKeyboardButton(
                        "Official Channel", url=f"https://t.me/creatorpavan"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "Source Code", url="https://t.me/CreatorPavanChat"
                    )
                ],
            ]
        ),
        disable_web_page_preview=True,
    )
