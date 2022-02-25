import asyncio

from pyrogram import Client, filters, __version__ as pyrover
from pyrogram.errors import FloodWait
from pytgcalls import (__version__ as pytover)
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, ChatJoinRequest
from oda.utils.filters import command

from oda.config import BOT_USERNAME

@Client.on_callback_query(filters.regex(pattern=r"^(Ayuu)$"))
async def ayuu(_, query: CallbackQuery):
    from_user = query.from_user
         return await query.answer(
            "You don't have enough permissions to perform this action.\n"
            + f"Hey Permission",
            show_alert=True,
        )
@Client.on_callback_query(filters.regex("skipdot"))
async def skipdot(_, CallbackQuery):
    return await CallbackQuery.answer(
            """
You do not have the necessary permissions to perform this action
• MANAGE VOICE CHAT
""",
            show_alert=True,
        )
@Client.on_message(
    command(["start", f"start@{BOT_USERNAME}"]) & filters.private & ~filters.edited
)
async def start_(c: Client, message: Message):
    await message.reply_text(
        f"""💖 **Welcome {message.from_user.mention()}""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Commands", callback_data="skipdot"),
                ],
                [
                    InlineKeyboardButton(
                        "Official Group", callback_data="ayuu"
                    ),
                    InlineKeyboardButton(
                        "Official Channel", url=f"https://t.me/creatorpavan"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "➕ Add me to your Group ➕",
                        url=f"https://t.me/RessoMusicBot?startgroup=true"
                    )
                ],
            ]
        ),
        disable_web_page_preview=True,
    )
