#agar ye file dekh rhe ho to importing and other things mein help kr do 
#millions Of Errors Are Here Plz Helo Kr Do 




#resso ka h he 

import aiofiles
import ffmpeg
import asyncio
import os
import shutil
import psutil
import subprocess
import requests
import aiohttp
import yt_dlp
import aiohttp
import random
import numpy as np

from os import path
from typing import Union
from asyncio import QueueEmpty
from PIL import Image, ImageFont, ImageDraw, ImageFilter
from PIL import ImageGrab
from typing import Callable

from pytgcalls import StreamType
from pytgcalls.types.input_stream import InputStream
from pytgcalls.types.input_stream import InputAudioStream

from youtube_search import YoutubeSearch

from pyrogram import Client, filters
from pyrogram.types import (
    Message,
    Voice,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
)
from pyrogram.errors import UserAlreadyParticipant, UserNotParticipant

from Codexun.tgcalls import calls, queues
from Codexun.tgcalls.calls import client as ASS_ACC
from Codexun.database.queue import (
    get_active_chats,
    is_active_chat,
    add_active_chat,
    remove_active_chat,
    music_on,
    is_music_playing,
    music_off,
)
from Codexun import app
import Codexun.tgcalls
from Codexun.tgcalls import youtube
from Codexun.config import (
    DURATION_LIMIT,
    que,
    SUDO_USERS,
    BOT_ID,
    ASSNAME,
    ASSUSERNAME,
    ASSID,
    SUPPORT,
    UPDATE,
    BOT_USERNAME,
)
from Codexun.utils.filters import command
from Codexun.utils.decorators import errors, sudo_users_only
from Codexun.utils.administrator import adminsOnly
from Codexun.utils.errors import DurationLimitError
from Codexun.utils.gets import get_url, get_file_name
from Codexun.modules.admins import member_permissions


# plus
chat_id = None
DISABLED_GROUPS = []
useer = "NaN"
flex = {}


def transcode(filename):
    ffmpeg.input(filename).output(
        "input.raw", format="s16le", acodec="pcm_s16le", ac=2, ar="48k"
    ).overwrite_output().run()
    os.remove(filename)


# Convert seconds to mm:ss
def convert_seconds(seconds):
    seconds = seconds % (24 * 3600)
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%02d:%02d" % (minutes, seconds)


# Convert hh:mm:ss to seconds
def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60**i for i, x in enumerate(reversed(stringt.split(":"))))



# Change image size
def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    newImage = image.resize((newWidth, newHeight))
    return newImage


async def generate_cover(requested_by, title, views, duration, thumbnail):
    async with aiohttp.ClientSession() as session:
        async with session.get(thumbnail) as resp:
            if resp.status == 200:
                f = await aiofiles.open("background.png", mode="wb")
                await f.write(await resp.read())
                await f.close()

    image = Image.open(f"background.png")
    black = Image.open("Utils/black.jpg")
    circle = Image.open("Utils/circle.png")
    image1 = changeImageSize(1280, 720, image)
    image1 = image1.filter(ImageFilter.BoxBlur(10))
    image2 = Image.blend(image1, black, 0.6)
    
    
    image2.save(f"final.png")
    os.remove(f"background.png")
    final = f"temp.png"
    return final
    


    

def others_markup(videoid, user_id):
    buttons = [
        [
            InlineKeyboardButton(text="▷", callback_data=f"resumevc"),
            InlineKeyboardButton(text="II", callback_data=f"pausevc"),
            InlineKeyboardButton(text="‣‣I", callback_data=f"skipvc"),
            InlineKeyboardButton(text="▢", callback_data=f"stopvc"),
        ],[
            InlineKeyboardButton(text="Fuck", callback_data=f"cls"),
        ],
        
    ]
    return buttons


play_keyboard = InlineKeyboardMarkup(
    [
        [
            
            InlineKeyboardButton("▷", callback_data="resumevc"),
            InlineKeyboardButton("II", callback_data="pausevc"),
            InlineKeyboardButton("‣‣I", callback_data="skipvc"),
            InlineKeyboardButton("▢", callback_data="stopvc"),
            
        ],
    ]
)
menu_keyboard = InlineKeyboardMarkup(
    [
        [
            
            InlineKeyboardButton("▷", callback_data="resumevc"),
            InlineKeyboardButton("II", callback_data="pausevc"),
            InlineKeyboardButton("‣‣I", callback_data="skipvc"),
            InlineKeyboardButton("▢", callback_data="stopvc"),
            
        ],[
            InlineKeyboardButton(text="Close Menu", callback_data=f"cls"),
        ],
    ]
)



@Client.on_callback_query(filters.regex("set_pause"))
async def cbpause(_, query: CallbackQuery):
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 Only admin with manage video chat permission that can tap this button !", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            if not await is_music_playing(chat_id):
                await query.answer("ℹ️ The music is already paused.", show_alert=True)
                return
            await calls.pause_stream(chat_id)
            await music_off(chat_id)
            await query.answer("⏸ The music has paused !\n\n» to resume the music click on resume button !", show_alert=True)
        except Exception as e:
            traceback.print_exc()
            await query.edit_message_text(f"🚫 **error:**\n\n`{e}`", reply_markup=close_mark)
    else:
        await query.answer("❌ nothing is currently streaming", show_alert=True)


@Client.on_callback_query(filters.regex("set_resume"))
async def cbresume(_, query: CallbackQuery):
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 Only admin with manage video chat permission that can tap this button !", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            if await is_music_playing(chat_id):
                await query.answer("ℹ️ The music is already resumed.", show_alert=True)
                return
            await calls.resume_stream(chat_id)
            await music_on(chat_id)
            await query.answer("▶️ The music has resumed !\n\n» to pause the music click on pause button !", show_alert=True)
        except Exception as e:
            traceback.print_exc()
            await query.edit_message_text(f"🚫 **error:**\n\n`{e}`", reply_markup=close_mark)
    else:
        await query.answer("❌ nothing is currently streaming", show_alert=True)


@Client.on_callback_query(filters.regex("set_stop"))
async def cbstop(_, query: CallbackQuery):
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 Only admin with manage video chat permission that can tap this button !", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            await calls.leave_group_call(chat_id)
            await remove_active_chat(chat_id)
            clear_queue(chat_id)
            await query.edit_message_text("✅ **this streaming has ended**", reply_markup=close_mark)
        except Exception as e:
            traceback.print_exc()
            await query.edit_message_text(f"🚫 **error:**\n\n`{e}`", reply_markup=close_mark)
    else:
        await query.answer("❌ nothing is currently streaming", show_alert=True)




# Veez ka h ye 
# Vstream Bhe H 


import re
import asyncio

from Codexun.config import ASSISTANT_NAME, BOT_USERNAME, IMG_1, IMG_2
from Codexun.utils.inline import stream_markup
from driver.design.thumbnail import thumb
from driver.design.chatname import CHAT_TITLE
from driver.filters import command, other_filters
from driver.queues import QUEUE, add_to_queue
from driver.veez import call_py, user
from pyrogram import Client
from pyrogram.errors import UserAlreadyParticipant, UserNotParticipant
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pytgcalls import StreamType
from pytgcalls.types.input_stream import AudioVideoPiped
from pytgcalls.types.input_stream.quality import (
    HighQualityAudio,
    HighQualityVideo,
    LowQualityVideo,
    MediumQualityVideo,
)
from youtubesearchpython import VideosSearch


def ytsearch(query: str):
    try:
        search = VideosSearch(query, limit=1).result()
        data = search["result"][0]
        songname = data["title"]
        url = data["link"]
        duration = data["duration"]
        thumbnail = f"https://i.ytimg.com/vi/{data['id']}/hqdefault.jpg"
        return [songname, url, duration, thumbnail]
    except Exception as e:
        print(e)
        return 0


async def ytdl(link):
    proc = await asyncio.create_subprocess_exec(
        "yt-dlp",
        "-g",
        "-f",
        "best[height<=?720][width<=?1280]",
        f"{link}",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    if stdout:
        return 1, stdout.decode().split("\n")[0]
    else:
        return 0, stderr.decode()


@Client.on_message(command(["vplay", f"vplay@{BOT_USERNAME}"]) & other_filters)
async def vplay(c: Client, m: Message):
    await m.delete()
    replied = m.reply_to_message
    chat_id = m.chat.id
    user_id = m.from_user.id
    if m.sender_chat:
        return await m.reply_text("you're an __Anonymous__ Admin !\n\n» revert back to user account from admin rights.")
    try:
        aing = await c.get_me()
    except Exception as e:
        return await m.reply_text(f"error:\n\n{e}")
    a = await c.get_chat_member(chat_id, aing.id)
    if a.status != "administrator":
        await m.reply_text(
            f"💡 To use me, I need to be an **Administrator** with the following **permissions**:\n\n» ❌ __Delete messages__\n» ❌ __Invite users__\n» ❌ __Manage video chat__\n\nOnce done, type /reload"
        )
        return
    if not a.can_manage_voice_chats:
        await m.reply_text(
        "💡 To use me, Give me the following permission below:"
        + "\n\n» ❌ __Manage video chat__\n\nOnce done, try again.")
        return
    if not a.can_delete_messages:
        await m.reply_text(
        "💡 To use me, Give me the following permission below:"
        + "\n\n» ❌ __Delete messages__\n\nOnce done, try again.")
        return
    if not a.can_invite_users:
        await m.reply_text(
        "💡 To use me, Give me the following permission below:"
        + "\n\n» ❌ __Add users__\n\nOnce done, try again.")
        return
    try:
        ubot = (await user.get_me()).id
        b = await c.get_chat_member(chat_id, ubot) 
        if b.status == "kicked":
            await c.unban_chat_member(chat_id, ubot)
            invitelink = await c.export_chat_invite_link(chat_id)
            if invitelink.startswith("https://t.me/+"):
                    invitelink = invitelink.replace(
                        "https://t.me/+", "https://t.me/joinchat/"
                    )
            await user.join_chat(invitelink)
    except UserNotParticipant:
        try:
            invitelink = await c.export_chat_invite_link(chat_id)
            if invitelink.startswith("https://t.me/+"):
                    invitelink = invitelink.replace(
                        "https://t.me/+", "https://t.me/joinchat/"
                    )
            await user.join_chat(invitelink)
        except UserAlreadyParticipant:
            pass
        except Exception as e:
            return await m.reply_text(
                f"❌ **userbot failed to join**\n\n**reason**: `{e}`"
            )

    if replied:
        if replied.video or replied.document:
            loser = await replied.reply("📥 **downloading...**")
            dl = await replied.download()
            link = replied.link
            if len(m.command) < 2:
                Q = 720
            else:
                pq = m.text.split(None, 1)[1]
                if pq == "720" or "480" or "360":
                    Q = int(pq)
                else:
                    Q = 720
                    await loser.edit(
                        "» __only 720, 480, 360 allowed__ \n💡 **now streaming video in 720p**"
                    )
            try:
                if replied.video:
                    songname = replied.video.file_name[:70]
                elif replied.document:
                    songname = replied.document.file_name[:70]
            except BaseException:
                songname = "Video"

            if chat_id in QUEUE:
                pos = add_to_queue(chat_id, songname, dl, link, "Video", Q)
                await loser.delete()
                requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                buttons = stream_markup(user_id)
                await m.reply_photo(
                    photo=f"{IMG_1}",
                    reply_markup=InlineKeyboardMarkup(buttons),
                    caption=f"💡 **Track added to queue »** `{pos}`\n\n🏷 **Name:** [{songname}]({link}) | `video`\n💭 **Chat:** `{chat_id}`\n🎧 **Request by:** {requester}",
                )
            else:
                if Q == 720:
                    amaze = HighQualityVideo()
                elif Q == 480:
                    amaze = MediumQualityVideo()
                elif Q == 360:
                    amaze = LowQualityVideo()
                await loser.edit("**Playing...**")
                await call_py.join_group_call(
                    chat_id,
                    AudioVideoPiped(
                        dl,
                        HighQualityAudio(),
                        amaze,
                    ),
                    stream_type=StreamType().local_stream,
                )
                add_to_queue(chat_id, songname, dl, link, "Video", Q)
                await loser.delete()
                requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                buttons = stream_markup(user_id)
                await m.reply_photo(
                    photo=f"{IMG_2}",
                    reply_markup=InlineKeyboardMarkup(others_markup),
                    caption=f"❰ 𝗙𝗮𝗹𝗹𝗲𝗻 ❘ 𝗠𝘂𝘀𝗶𝗰 ❱ ❤ 𝗡𝗼𝘄 🤘 𝗣𝗹𝗮𝘆𝗶𝗻𝗴 📀 𝗙𝗿𝗼𝗺 🔊 𝗖𝗿𝗲𝗮𝘁𝗼𝗿 🚩 𝗣𝗮𝘃𝗮𝗻 😎 𝗦𝗲𝗿𝘃𝗲𝗿...🤞\n**User :** {requester}\n**Stream type :** `Video`",
                )
        else:
            if len(m.command) < 2:
                await m.reply(
                    "» reply to an **video file** or **give something to search.**"
                )
            else:
                loser = await c.send_message(chat_id, "🔍")
                query = m.text.split(None, 1)[1]
                search = ytsearch(query)
                Q = 720
                amaze = HighQualityVideo()
                if search == 0:
                    await loser.edit("❌ **no results found.**")
                else:
                    songname = search[0]
                    title = search[0]
                    url = search[1]
                    duration = search[2]
                    thumbnail = search[3]
                    userid = m.from_user.id
                    gcname = m.chat.title
                    ctitle = await CHAT_TITLE(gcname)
                    image = await thumb(thumbnail, title, userid, ctitle)
                    veez, ytlink = await ytdl(url)
                    if veez == 0:
                        await loser.edit(f"❌ yt-dl issues detected\n\n» `{ytlink}`")
                    else:
                        if chat_id in QUEUE:
                            pos = add_to_queue(
                                chat_id, songname, ytlink, url, "Video", Q
                            )
                            await loser.delete()
                            requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                            buttons = stream_markup(user_id)
                            await m.reply_photo(
                                photo=image,
                                reply_markup=InlineKeyboardMarkup(buttons),
                                caption=f"💡 **Track added to queue »** `{pos}`\n\n🏷 **Name:** [{songname}]({url}) | `video`\n⏱ **Duration:** `{duration}`\n🎧 **Request by:** {requester}",
                            )
                        else:
                            try:
                                await loser.edit("**Playing...**")
                                await call_py.join_group_call(
                                    chat_id,
                                    AudioVideoPiped(
                                        ytlink,
                                        HighQualityAudio(),
                                        amaze,
                                    ),
                                    stream_type=StreamType().local_stream,
                                )
                                add_to_queue(chat_id, songname, ytlink, url, "Video", Q)
                                await loser.delete()
                                requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                                buttons = stream_markup(user_id)
                                await m.reply_photo(
                                    photo=image,
                                    reply_markup=InlineKeyboardMarkup(others_markup),
                                    caption=f"❰ 𝗙𝗮𝗹𝗹𝗲𝗻 ❘ 𝗠𝘂𝘀𝗶𝗰 ❱ ❤ 𝗡𝗼𝘄 🤘 𝗣𝗹𝗮𝘆𝗶𝗻𝗴 📀 𝗙𝗿𝗼𝗺 🔊 𝗖𝗿𝗲𝗮𝘁𝗼𝗿 🚩 𝗣𝗮𝘃𝗮𝗻 😎 𝗦𝗲𝗿𝘃𝗲𝗿...🤞\n**User :** {requester}\n**Stream type :** `Video`",
                                )
                            except Exception as ep:
                                await loser.delete()
                                await m.reply_text(f"🚫 error: `{ep}`")

    else:
        if len(m.command) < 2:
            await m.reply(
                "» reply to an **video file** or **give something to search.**"
            )
        else:
            loser = await c.send_message(chat_id, "🔍")
            query = m.text.split(None, 1)[1]
            search = ytsearch(query)
            Q = 720
            amaze = HighQualityVideo()
            if search == 0:
                await loser.edit("❌ **no results found.**")
            else:
                songname = search[0]
                title = search[0]
                url = search[1]
                duration = search[2]
                thumbnail = search[3]
                userid = m.from_user.id
                gcname = m.chat.title
                ctitle = await CHAT_TITLE(gcname)
                image = await thumb(thumbnail, title, userid, ctitle)
                veez, ytlink = await ytdl(url)
                if veez == 0:
                    await loser.edit(f"❌ yt-dl issues detected\n\n» `{ytlink}`")
                else:
                    if chat_id in QUEUE:
                        pos = add_to_queue(chat_id, songname, ytlink, url, "Video", Q)
                        await loser.delete()
                        requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                        buttons = stream_markup(user_id)
                        await m.reply_photo(
                            photo=image,
                            reply_markup=InlineKeyboardMarkup(buttons),
                            caption=f"💡 **Track added to queue »** `{pos}`\n\n🏷 **Name:** [{songname}]({url}) | `video`\n⏱ **Duration:** `{duration}`\n🎧 **Request by:** {requester}",
                        )
                    else:
                        try:
                            await loser.edit("**Playing...**")
                            await call_py.join_group_call(
                                chat_id,
                                AudioVideoPiped(
                                    ytlink,
                                    HighQualityAudio(),
                                    amaze,
                                ),
                                stream_type=StreamType().local_stream,
                            )
                            add_to_queue(chat_id, songname, ytlink, url, "Video", Q)
                            await loser.delete()
                            requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                            buttons = stream_markup(user_id)
                            await m.reply_photo(
                                photo=image,
                                reply_markup=InlineKeyboardMarkup(others_markup),
                                caption=f"❰ 𝗙𝗮𝗹𝗹𝗲𝗻 ❘ 𝗠𝘂𝘀𝗶𝗰 ❱ ❤ 𝗡𝗼𝘄 🤘 𝗣𝗹𝗮𝘆𝗶𝗻𝗴 📀 𝗙𝗿𝗼𝗺 🔊 𝗖𝗿𝗲𝗮𝘁𝗼𝗿 🚩 𝗣𝗮𝘃𝗮𝗻 😎 𝗦𝗲𝗿𝘃𝗲𝗿...🤞\n**User :** {requester}\n**Stream type :** `Video`",
                            )
                        except Exception as ep:
                            await loser.delete()
                            await m.reply_text(f"🚫 error: `{ep}`")


@Client.on_message(command(["vstream", f"vstream@{BOT_USERNAME}"]) & other_filters)
async def vstream(c: Client, m: Message):
    await m.delete()
    chat_id = m.chat.id
    user_id = m.from_user.id
    if m.sender_chat:
        return await m.reply_text("you're an __Anonymous__ Admin !\n\n» revert back to user account from admin rights.")
    try:
        aing = await c.get_me()
    except Exception as e:
        return await m.reply_text(f"error:\n\n{e}")
    a = await c.get_chat_member(chat_id, aing.id)
    if a.status != "administrator":
        await m.reply_text(
            f"💡 To use me, I need to be an **Administrator** with the following **permissions**:\n\n» ❌ __Delete messages__\n» ❌ __Invite users__\n» ❌ __Manage video chat__\n\nOnce done, type /reload"
        )
        return
    if not a.can_manage_voice_chats:
        await m.reply_text(
        "💡 To use me, Give me the following permission below:"
        + "\n\n» ❌ __Manage video chat__\n\nOnce done, try again.")
        return
    if not a.can_delete_messages:
        await m.reply_text(
        "💡 To use me, Give me the following permission below:"
        + "\n\n» ❌ __Delete messages__\n\nOnce done, try again.")
        return
    if not a.can_invite_users:
        await m.reply_text(
        "💡 To use me, Give me the following permission below:"
        + "\n\n» ❌ __Add users__\n\nOnce done, try again.")
        return
    try:
        ubot = (await user.get_me()).id
        b = await c.get_chat_member(chat_id, ubot) 
        if b.status == "kicked":
            await c.unban_chat_member(chat_id, ubot)
            invitelink = await c.export_chat_invite_link(chat_id)
            if invitelink.startswith("https://t.me/+"):
                    invitelink = invitelink.replace(
                        "https://t.me/+", "https://t.me/joinchat/"
                    )
            await user.join_chat(invitelink)
    except UserNotParticipant:
        try:
            invitelink = await c.export_chat_invite_link(chat_id)
            if invitelink.startswith("https://t.me/+"):
                    invitelink = invitelink.replace(
                        "https://t.me/+", "https://t.me/joinchat/"
                    )
            await user.join_chat(invitelink)
        except UserAlreadyParticipant:
            pass
        except Exception as e:
            return await m.reply_text(
                f"❌ **userbot failed to join**\n\n**reason**: `{e}`"
            )

    if len(m.command) < 2:
        await m.reply("» give me a live-link/m3u8 url/youtube link to stream.")
    else:
        if len(m.command) == 2:
            link = m.text.split(None, 1)[1]
            Q = 720
            loser = await c.send_message(chat_id, "🔄 **Starting Stream...**")
        elif len(m.command) == 3:
            op = m.text.split(None, 1)[1]
            link = op.split(None, 1)[0]
            quality = op.split(None, 1)[1]
            if quality == "720" or "480" or "360":
                Q = int(quality)
            else:
                Q = 720
                await m.reply(
                    "» __only 720, 480, 360 allowed__ \n💡 **now streaming video in 720p**"
                )
            loser = await c.send_message(chat_id, "🔄 **Starting Stream...**")
        else:
            await m.reply("**/vstream {link} {720/480/360}**")

        regex = r"^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+"
        match = re.match(regex, link)
        if match:
            veez, livelink = await ytdl(link)
        else:
            livelink = link
            veez = 1

        if veez == 0:
            await loser.edit(f"❌ yt-dl issues detected\n\n» `{livelink}`")
        else:
            if chat_id in QUEUE:
                pos = add_to_queue(chat_id, "Live Stream", livelink, link, "Video", Q)
                await loser.delete()
                requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                buttons = stream_markup(user_id)
                await m.reply_photo(
                    photo=f"{IMG_1}",
                    reply_markup=InlineKeyboardMarkup(buttons),
                    caption=f"💡 **Track added to queue »** `{pos}`\n\n💭 **Chat:** `{chat_id}`\n🎧 **Request by:** {requester}",
                )
            else:
                if Q == 720:
                    amaze = HighQualityVideo()
                elif Q == 480:
                    amaze = MediumQualityVideo()
                elif Q == 360:
                    amaze = LowQualityVideo()
                try:
                    await loser.edit("🔄 **Playing...**")
                    await call_py.join_group_call(
                        chat_id,
                        AudioVideoPiped(
                            livelink,
                            HighQualityAudio(),
                            amaze,
                        ),
                        stream_type=StreamType().live_stream,
                    )
                    add_to_queue(chat_id, "Live Stream", livelink, link, "Video", Q)
                    await loser.delete()
                    requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                    buttons = stream_markup(user_id)
                    await m.reply_photo(
                        photo=f"{IMG_2}",
                        reply_markup=InlineKeyboardMarkup(buttons),
                        caption=f"💡 **[Video live]({link}) stream started.**\n\n💭 **Chat:** `{chat_id}`\n💡 **Status:** `Playing`\n🎧 **Request by:** {requester}",
                    )
                except Exception as ep:
                    await loser.delete()
                    await m.reply_text(f"🚫 error: `{ep}`")

