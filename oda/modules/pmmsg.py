from pyrogram import Client
from driver.core import user as USER
from pyrogram import filters
from pyrogram.types import Chat, Message, User


@USER.on_message(filters.text & filters.private & ~filters.me & ~filters.bot)
async def pmPermit(client: USER, message: Message):
  await USER.send_message(message.chat.id,"🔰ᴛʜɪs ɪs ᴀssɪsᴛᴀɴᴛ ᴏғ @RessoMusicBot ᴊᴏɪɴ @TheCreatorPavan ғᴏʀ ᴜᴘᴅᴀᴛᴇᴅ🔰")
  return
