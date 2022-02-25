import asyncio

from pyrogram import Client, filters, __version__ as pyrover
from pyrogram.errors import FloodWait
from pytgcalls import (__version__ as pytover)
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, ChatJoinRequest
from oda.utils.filters import command

from oda.config import BOT_USERNAME

@Client.on_callback_query(filters.regex("cbsetting"))
async def cbsetting(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""**ᴘᴀᴠᴀɴ ꜱᴇᴛᴛɪɴɢꜱ ᴄᴏᴍᴍᴀɴᴅꜱ :**
» /pause - ꜰᴏʀ ᴘᴀᴜꜱɪɴɢ ꜱᴛʀᴇᴀᴍɪɴɢ. 
» /resume - ꜰᴏʀ ʀᴇꜱᴜᴍᴇ ꜱᴛʀᴇᴀᴍɪɴɢ. 
» /skip - ꜰᴏʀ ꜱᴋɪᴘᴘɪɴɢ ᴄᴜʀʀᴇɴᴛ ꜱᴏɴɢ ᴀɴᴅ ᴘʟᴀʏɪɴɢ ɴᴇxᴛ ꜱᴏɴɢ. 
» /mute - ꜰᴏʀ ᴍᴜᴛᴜɪɴɢ ᴀꜱꜱɪꜱᴛᴀɴᴛ ɪɴ ᴠᴄ. 
» /unmute - ꜰᴏʀ ᴜɴᴍᴜᴛᴇ ᴀꜱꜱɪꜱᴛᴀɴᴛ ɪɴ ᴠᴄ. 
» /end - ꜰᴏʀ ᴇɴᴅ ꜱᴛʀᴇᴀᴍɪɴɢ. 
**© @TheCreatorPavan**""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙  ʙᴀᴄᴋ ᴛᴏ ʜᴏᴍᴇ", callback_data="cbcmds")]]
        ),
    )

@Client.on_message(command("start") & filters.private & ~filters.edited)
async def start_(client: Client, message: Message):
    await message.reply_photo(
        photo=f"https://telegra.ph/file/81671ed0156630ad5db4e.png",
        caption=f"""What a fuck bro""",
    reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "➕ ❰ ᴊᴏɪɴ ʜᴇʀᴇ ғᴏʀ ᴜᴘᴅᴀᴛᴇs ❱ ➕", callback_data="cbsetting")
                ]
                
           ]
        ),
    )
