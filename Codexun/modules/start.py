import asyncio

from pyrogram import Client, filters, __version__ as pyrover
from pyrogram.errors import FloodWait
from pytgcalls import (__version__ as pytover)
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, ChatJoinRequest
from Codexun.utils.filters import command

from Codexun.config import BOT_USERNAME





import re, os, random, asyncio, html,configparser,pyrogram, subprocess, requests, time, traceback, logging, telethon, csv, json, sys
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from asyncio.exceptions import TimeoutError
from pyrogram.errors import SessionPasswordNeeded, FloodWait, PhoneNumberInvalid, ApiIdInvalid, PhoneCodeInvalid, PhoneCodeExpired, UserNotParticipant
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant
from telethon.client.chats import ChatMethods
from csv import reader
from telethon.sync import TelegramClient
from telethon import functions, types, TelegramClient, connection, sync, utils, errors
from telethon.tl.functions.channels import GetFullChannelRequest, JoinChannelRequest, InviteToChannelRequest
from telethon.errors import SessionPasswordNeededError
from telethon.errors.rpcerrorlist import PhoneCodeExpiredError, PhoneCodeInvalidError, PhoneNumberBannedError, PhoneNumberInvalidError, UserBannedInChannelError, PeerFloodError, UserPrivacyRestrictedError, ChatWriteForbiddenError, UserAlreadyParticipantError,  UserBannedInChannelError, UserAlreadyParticipantError,  UserPrivacyRestrictedError, ChatAdminRequiredError
from telethon.sessions import StringSession
from pyrogram import Client,filters
from pyrogram.types import (
    Message,
    Voice,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
)
from pyromod import listen

APP_ID = "18854932"
API_HASH = "9d91a01f9cc8086e004c398c96c22d89"
BOT_TOKEN = "5181191526:AAEiUPlIDTs1M2RyNfFwX0_J4K9xZczbAvY"
UPDATES_CHANNEL = "Codexun"
OWNER= [2056407064]
PREMIUM=[2056407064]
app = pyrogram.Client("app", api_id=APP_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

    

# ------------------------------- Subscribe --------------------------------- #
async def Subscribe(lel, message):
   update_channel = UPDATES_CHANNEL
   if update_channel:
      try:
         user = await app.get_chat_member(update_channel, message.chat.id)
         if user.status == "kicked":
            await app.send_message(chat_id=message.chat.id,text="Sorry Sir, You are Banned. Contact My [Support Group](https://t.me/TeamCodexun).", parse_mode="markdown", disable_web_page_preview=True)
            return 1
      except UserNotParticipant:
         await app.send_message(chat_id=message.chat.id, text="**You Need To Join My Update Channel For Using Me and Working Properly.\n\njoin and press /start for check!**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🤖 Join Update Channel 🤖", url=f"https://t.me/{update_channel}")]]), parse_mode="markdown")
         return 1
      except Exception:
         await app.send_message(chat_id=message.chat.id, text="**Something Went Wrong. Contact My [Support Group](https://t.me/TeamCodexun).**", parse_mode="markdown", disable_web_page_preview=True)
         return 1



# ------------------------------- Start --------------------------------- #
@app.on_message(filters.private & filters.command(["start"]))
async def start(lel, message):
   a= await Subscribe(lel, message)
   if a==1:
      return
   if not os.path.exists(f"Users/{message.from_user.id}/phone.csv"):
      os.mkdir(f'./Users/{message.from_user.id}')
      open(f"Users/{message.from_user.id}/phone.csv","w")
   id = message.from_user.id
   user_name = '@' + message.from_user.username if message.from_user.username else None
   await add_user(id, user_name)
   but = InlineKeyboardMarkup([[InlineKeyboardButton("User Panel 👤", callback_data="userpanel"), InlineKeyboardButton("Offer Zone 🎁", callback_data="offerzone") ],[InlineKeyboardButton("Details 📂", callback_data="details"), InlineKeyboardButton("Premium 💳", callback_data="premium")],[InlineKeyboardButton("How to Use 📋", callback_data="howto")]])
   await message.reply_photo(
        photo=f"https://telegra.ph/file/a5c63618c33ab9208914d.jpg",
        caption=f"""**Welcome {message.from_user.mention()} 👋**\n\nThis is the Members Increaser Bot, a bot made for helping to add unlimited members in your super group.\n\nThere is no need of any type of script or anything else, you can simply use this bot and increase your groups member as you need.\n\n**Use the given buttons for more..**""", reply_markup=but)






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
                        "About", callback_data="cbabout")
                ],
                [
                    InlineKeyboardButton(
                        "Basic Guide", callback_data="cbguide")
                ],
                [
                    InlineKeyboardButton(
                        "✚ Add Bot in Your Group ✚", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")
                ]
           ]
        ),
    )
