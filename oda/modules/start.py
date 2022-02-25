
import asyncio

from pyrogram import Client, filters, __version__ as pyrover
from pyrogram.errors import FloodWait
from pytgcalls import (__version__ as pytover)
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, ChatJoinRequest
from oda.utils.filters import command

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
                    InlineKeyboardButton("𝖢𝗈𝗆𝗆𝖺𝗇𝖽𝗌", callback_data="command_list"),
                ],
                [
                    InlineKeyboardButton(
                        "𝖲𝗎𝗉𝗉𝗈𝗋𝗍 𝖦𝗋𝗈𝗎𝗉", url=f"https://t.me/CreatorPavanChat"
                    ),
                    InlineKeyboardButton(
                        "𝖴𝗉𝖽𝖺𝗍𝖾𝗌 𝖢𝗁𝖺𝗇𝗇𝖾𝗅", url=f"https://t.me/creatorpavan"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "𝖠𝖽𝖽 𝖬𝖾 𝖳𝗈 𝖸𝗈𝗎𝗋 𝖦𝗋𝗈𝗎𝗉",
                        url=f"https://t.me/RessoMusicBot?startgroup=true"
                    )
                ],
            ]
        ),
        disable_web_page_preview=True,
    )
