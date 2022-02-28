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


def truncate(text):
    list = text.split(" ")
    text1 = ""
    text2 = ""    
    for i in list:
        if len(text1) + len(i) < 24:        
            text1 += " " + i
        elif len(text2) + len(i) < 24:        
            text2 += " " + i

    text1 = text1.strip()
    text2 = text2.strip()     
    return [text1,text2]

def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    newImage = image.resize((newWidth, newHeight))
    return newImage


async def generate_cover(requested_by, title, views, duration, thumbnail, userid):
    async with aiohttp.ClientSession() as session:
        async with session.get(thumbnail) as resp:
            if resp.status == 200:
                f = await aiofiles.open(f"cache/thumb{userid}.jpg", mode="wb")
                await f.write(await resp.read())
                await f.close()
    
    image = Image.open(f"cache/thumb{userid}.jpg")
    black = Image.open("Utils/black.jpg")
    circle = Image.open("Utils/circle.png")
    image1 = changeImageSize(1280, 720, image)
    image1 = image1.filter(ImageFilter.BoxBlur(20))
    image2 = Image.blend(image1,black,0.6)

    # Cropping circle from thubnail
    image3 = image.crop((280,0,1000,720))
    lum_img = Image.new('L', [720,720] , 0)
    draw = ImageDraw.Draw(lum_img)
    draw.pieslice([(0,0), (720,720)], 0, 360, fill = 255, outline = "white")
    img_arr =np.array(image3)
    lum_img_arr =np.array(lum_img)
    final_img_arr = np.dstack((img_arr,lum_img_arr))
    image3 = Image.fromarray(final_img_arr)
    image3 = image3.resize((600,600))

    image2.paste(image3, (50,70), mask = image3)
    image2.paste(circle, (0,0), mask = circle)

    # fonts
    font1 = ImageFont.truetype(r'Utils/arial_bold.ttf', 30)
    font2 = ImageFont.truetype(r'Utils/arial_black.ttf', 60)
    font3 = ImageFont.truetype(r'Utils/arial_black.ttf', 40)
    font4 = ImageFont.truetype(r'Utils/arial_bold.ttf', 35)

    image4 = ImageDraw.Draw(image2)
    
    # title
    title1 = truncate(title)
    image4.text((670, 300), text=title1[0], fill="white", font = font3, align ="left") 
    image4.text((670, 350), text=title1[1], fill="white", font = font3, align ="left") 

    # description
    views = f"Views : {views}"
    duration = f"Duration : {duration} Mins"

    image4.text((670, 450), text=views, fill="white", font = font4, align ="left") 
    image4.text((670, 500), text=duration, fill="white", font = font4, align ="left") 

    image2.save(f"cache/final{userid}.png")
    os.remove(f"cache/thumb{userid}.jpg")
    final = f"cache/final{userid}.png"
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

@Client.on_message(command(["menu", "settings"]) & ~filters.edited)
async def menu(client: Client, message: Message):
    await message.reply_photo(
        photo=f"https://telegra.ph/file/e594d98181c2f54b872fd.jpg",
        caption=f"""**Hey {message.from_user.mention()}** 👋
This the menu section where you can manage music playing on your groups voice chat. Use the given buttons for manage!""",
    reply_markup=menu_keyboard
    )

@Client.on_callback_query(filters.regex("skipvc"))
async def skipvc(_, CallbackQuery):
    a = await app.get_chat_member(
        CallbackQuery.message.chat.id, CallbackQuery.from_user.id
    )
    if not a.can_manage_voice_chats:
        return await CallbackQuery.answer(
            """
Only admin with manage voice chat permission can do this.
""",
            show_alert=True,
        )
    CallbackQuery.from_user.first_name
    chat_id = CallbackQuery.message.chat.id
    chat_title = CallbackQuery.message.chat.title
    if await is_active_chat(chat_id):
            user_id = CallbackQuery.from_user.id
            await remove_active_chat(chat_id)
            user_name = CallbackQuery.from_user.first_name
            rpk = "[" + user_name + "](tg://user?id=" + str(user_id) + ")"
            await CallbackQuery.answer()
            await CallbackQuery.message.reply(
                f"""
**Skip Button Used By** {rpk}
• No more songs in Queue
`Leaving Voice Chat..`
"""
            )
            await calls.pytgcalls.leave_group_call(chat_id)
            return
            await CallbackQuery.answer("Voice Chat Skip.!", show_alert=True)     

@Client.on_callback_query(filters.regex("pausevc"))
async def pausevc(_, CallbackQuery):
    a = await app.get_chat_member(
        CallbackQuery.message.chat.id, CallbackQuery.from_user.id
    )
    if not a.can_manage_voice_chats:
        return await CallbackQuery.answer(
            "Only admin with manage voice chat permission can do this.",
            show_alert=True,
        )
    CallbackQuery.from_user.first_name
    chat_id = CallbackQuery.message.chat.id
    if await is_active_chat(chat_id):
        if await is_music_playing(chat_id):
            await music_off(chat_id)
            await calls.pytgcalls.pause_stream(chat_id)
            await CallbackQuery.answer("Music Paused Successfully.", show_alert=True)
            
        else:
            await CallbackQuery.answer(f"Nothing is playing on voice chat!", show_alert=True)
            return
    else:
        await CallbackQuery.answer(f"Nothing is playing in on voice chat!", show_alert=True)


@Client.on_callback_query(filters.regex("resumevc"))
async def resumevc(_, CallbackQuery):
    a = await app.get_chat_member(
        CallbackQuery.message.chat.id, CallbackQuery.from_user.id
    )
    if not a.can_manage_voice_chats:
        return await CallbackQuery.answer(
            """
Only admin with manage voice chat permission can do this.
""",
            show_alert=True,
        )
    CallbackQuery.from_user.first_name
    chat_id = CallbackQuery.message.chat.id
    if await is_active_chat(chat_id):
        if await is_music_playing(chat_id):
            await CallbackQuery.answer(
                "Nothing is paused in the voice chat.",
                show_alert=True,
            )
            return
        else:
            await music_on(chat_id)
            await calls.pytgcalls.resume_stream(chat_id)
            await CallbackQuery.answer("Music resumed successfully.", show_alert=True)
            
    else:
        await CallbackQuery.answer(f"Nothing is playing.", show_alert=True)


@Client.on_callback_query(filters.regex("stopvc"))
async def stopvc(_, CallbackQuery):
    a = await app.get_chat_member(
        CallbackQuery.message.chat.id, CallbackQuery.from_user.id
    )
    if not a.can_manage_voice_chats:
        return await CallbackQuery.answer(
            "Only admin with manage voice chat permission can do this.",
            show_alert=True,
        )
    CallbackQuery.from_user.first_name
    chat_id = CallbackQuery.message.chat.id
    if await is_active_chat(chat_id):
        
        try:
            await calls.pytgcalls.leave_group_call(chat_id)
        except Exception:
            pass
        await remove_active_chat(chat_id)
        await CallbackQuery.answer("Music stream ended.", show_alert=True)
        user_id = CallbackQuery.from_user.id
        user_name = CallbackQuery.from_user.first_name
        rpk = "[" + user_name + "](tg://user?id=" + str(user_id) + ")"
        await CallbackQuery.message.reply(f"**• Music successfully stopped by {rpk}.**")
    else:
        await CallbackQuery.answer(f"Nothing is playing on voice chat.", show_alert=True)


@Client.on_callback_query(filters.regex("cbcmnds"))
async def cbcmnds(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""**Resso Music Bot Commands 💡**


• /play (song name) 
- For playing music

• /pause 
- For pausing music

• /resume 
- For resuming music

• /skip 
- For skipping current song

• /search (song name) 
- For searching music

• /song (song name)
- For download music

• /menu or /settings
- For open menu settings

Powered by **Resso Music** !""",
        reply_markup=InlineKeyboardMarkup(
            [
              [InlineKeyboardButton("Menu Buttons", callback_data="cbmenu")],
              [InlineKeyboardButton("🔙  Back Home", callback_data="cbhome")]]
        ),
    )

@Client.on_callback_query(filters.regex("cbabout"))
async def cbabout(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""**About Resso Music Bot 💡**

Resso Music Bot is the bot designed by some noobs team for playing a high quality and unbreakable music in your groups voice chat.

This bot helps you to play music, to search music from youtube and to download music from youtube server and many more features related to telegram voice chat feature.

**Thanks !**""",
        reply_markup=InlineKeyboardMarkup(
            [
            [InlineKeyboardButton("Need Help", callback_data="cbhelp")],
            [InlineKeyboardButton("🔙  Back Home", callback_data="cbhome")]]
        ),
    )

@Client.on_callback_query(filters.regex("cbmenu"))
async def cbmenu(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""**About Menu Buttons 💡**

After you played your song some menu buttons will be comes to manage your music playing on voice chat. They are as follows :

• ▷ 
- Resume Music
• II 
- Pause Music
• ▢  
- End Music
• ‣‣ 
- Skip Music

You can also open this menu through /menu and /settings command.

**Only admins can use this buttons 📍**""",
        reply_markup=InlineKeyboardMarkup(
            [
            [InlineKeyboardButton("🔙  Back Home", callback_data="cbcmnds")]]
        ),
    )
@Client.on_callback_query(filters.regex("cbhelp"))
async def cbhelp(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""**Need Help 💡**

**[Resso Music Bot](https://t.me/RessoMusicBot)**

**• Bot Managed By** 
**- #one_noob**

**• Special Thanks**
**- #no_need**

**Note : Some kangers thinking this bot is deployed from their repo. Fuck off bruh, You really great !**""",
        reply_markup=InlineKeyboardMarkup(
            [
            [InlineKeyboardButton("Contact If really Need Help", url=f"https://t.me/RessoSupportBot")],
            [InlineKeyboardButton("🔙  Back Home", callback_data="cbabout")]]
        ),
    )
@Client.on_callback_query(filters.regex("cbguide"))
async def cbguide(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""**Read Basic Guide Carefully 💡**

• First add this bot in your group

• Make a bot admin

• Give needed admin permission

• Type /reload in your group

• Start your groups voice chat

• Now play your song and enjoy !""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("Try Inline Search", switch_inline_query_current_chat="")],
              [InlineKeyboardButton("🔙  Back Home", callback_data="cbhome")]]
        ),
    )

@Client.on_callback_query(filters.regex("cbhome"))
async def cbhome(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""**Welcome [{query.message.chat.first_name}](tg://user?id={query.message.chat.id})** 👋

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

@Client.on_callback_query(filters.regex(pattern=r"^(cls)$"))
async def closed(_, query: CallbackQuery):
    from_user = query.from_user
    permissions = await member_permissions(query.message.chat.id, from_user.id)
    permission = "can_restrict_members"
    if permission not in permissions:
        return await query.answer(
            "You don't have enough permissions to perform this action.",
            show_alert=True,
        )
    await query.message.delete()


# play
@Client.on_message(
    command(["play", f"play@{BOT_USERNAME}"])
    & filters.group
    & ~filters.edited
    & ~filters.forwarded
    & ~filters.via_bot
)
async def play(_, message: Message):
    global que
    global useer
    user_id = message.from_user.id
    if message.sender_chat:
        return await message.reply_text(
            "🔴 __You're an **Anonymous Admin**!__\n│\n╰ Revert back to user account from admin rights."
        )

    if message.chat.id in DISABLED_GROUPS:
        await message.reply(
            "🔴 __**Music player is turned off, ask the admin to turn on it on!**__"
        )
      

        return
    lel = await message.reply("**Processing started..**")

    chid = message.chat.id

    c = await app.get_chat_member(message.chat.id, BOT_ID)
    if c.status != "administrator":
        await lel.edit(
            f"**Make me admin first !**"
        )
        return
    if not c.can_manage_voice_chats:
        await lel.edit(
            "**Give me** `manage voice chat` **admin permission.**"
        )
        return
    if not c.can_delete_messages:
        await lel.edit(
            "**Give me** `Delete massages` **admin permission.**"
        )
        return
    if not c.can_invite_users:
        await lel.edit(
            "**Give me** `invite user` **admin permission.**"
        )
        return
    if not c.can_restrict_members:
        await lel.edit(
            "**Give me** `ban user` **admin permission.**"
        )
        return

    try:
        b = await app.get_chat_member(message.chat.id, ASSID)
        if b.status == "kicked":
            await message.reply_text(
                f"🔴 {ASSNAME} (@{ASSUSERNAME}) is banned in your chat **{message.chat.title}**\n\nUnban it first to use music"
            )
            return
    except UserNotParticipant:
        if message.chat.username:
            try:
                await ASS_ACC.join_chat(f"{message.chat.username}")
                await message.reply(
                    f"**Resso Music Assistant joined !**",
                )
                await remove_active_chat(chat_id)
            except Exception as e:
                await message.reply_text(
                    f"**Resso Assistant failed to join** Add @RessoMusicAssistant manually in your group.\n\n**Reason**:{e}"
                )
                return
        else:
            try:
                invite_link = await message.chat.export_invite_link()
                if "+" in invite_link:
                    kontol = (invite_link.replace("+", "")).split("t.me/")[1]
                    link_bokep = f"https://t.me/joinchat/{kontol}"
                await ASS_ACC.join_chat(link_bokep)
                await message.reply(
                    f"**Resso Assistant joined successfully**",
                )
                await remove_active_chat(message.chat.id)
            except UserAlreadyParticipant:
                pass
            except Exception as e:
                return await message.reply_text(
                    f"**Assistant failed to join** Add @RessoMusicAssistant manually in your group.\n\n**Reason**:{e}"
                )

    await message.delete()
    audio = (
        (message.reply_to_message.audio or message.reply_to_message.voice)
        if message.reply_to_message
        else None
    )
    url = get_url(message)

    if audio:
        if round(audio.duration / 60) > DURATION_LIMIT:
            raise DurationLimitError(
                f"💡 Videos longer than {DURATION_LIMIT} minutes aren't allowed to play!"
            )

        file_name = get_file_name(audio)
        url = f"https://t.me/{UPDATE}"
        title = audio.title
        thumb_name = "https://telegra.ph/file/a7adee6cf365d74734c5d.png"
        thumbnail = thumb_name
        duration = round(audio.duration / 60)
        views = "Locally added"

        keyboard = InlineKeyboardMarkup(
    [
        
       [
            InlineKeyboardButton("03:45----------01:15", callback_data="nothing"),
        ],[
            InlineKeyboardButton("▷", callback_data="resumevc"),
            InlineKeyboardButton("II", callback_data="pausevc"),
            InlineKeyboardButton("‣‣I", callback_data="skipvc"),
            InlineKeyboardButton("▣", callback_data="stopvc"),
        ],[
            InlineKeyboardButton("Menu", callback_data="menu"),
            InlineKeyboardButton("Close", callback_data="cls"),
        ],
        
    ]
)

        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)
        file_path = await oda.tgcalls.convert(
            (await message.reply_to_message.download(file_name))
            if not path.isfile(path.join("downloads", file_name))
            else file_name
        )

    elif url:
        try:
            results = YoutubeSearch(url, max_results=1).to_dict()
            # print results
            title = results[0]["title"][:12]
            thumbnail = results[0]["thumbnails"][0]
            thumb_name = f"thumb{title}.jpg"
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, "wb").write(thumb.content)
            duration = results[0]["duration"]
            url_suffix = results[0]["url_suffix"]
            views = results[0]["views"]
            durl = url
            durl = durl.replace("youtube", "youtubepp")

            secmul, dur, dur_arr = 1, 0, duration.split(":")
            for i in range(len(dur_arr) - 1, -1, -1):
                dur += int(dur_arr[i]) * secmul
                secmul *= 60

            keyboard = InlineKeyboardMarkup(
    [
        
       [
            InlineKeyboardButton("03:45----------01:15", callback_data="nothing"),
        ],[
            InlineKeyboardButton("▷", callback_data="resumevc"),
            InlineKeyboardButton("II", callback_data="pausevc"),
            InlineKeyboardButton("‣‣I", callback_data="skipvc"),
            InlineKeyboardButton("▣", callback_data="stopvc"),
        ],[
            InlineKeyboardButton("Menu", callback_data="menu"),
            InlineKeyboardButton("Close", callback_data="cls"),
        ],
        
    ]
)

        except Exception as e:
            title = "NaN"
            thumb_name = "https://telegra.ph/file/a7adee6cf365d74734c5d.png"
            duration = "NaN"
            views = "NaN"
            keyboard = InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="YouTube 🎬", url="https://youtube.com")]]
            )

        if (dur / 60) > DURATION_LIMIT:
            await lel.edit(
                f"💡 Videos longer than {DURATION_LIMIT} minutes aren't allowed to play!"
            )
            return
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)

        def my_hook(d):
            if d["status"] == "downloading":
                percentage = d["_percent_str"]
                per = (str(percentage)).replace(".", "", 1).replace("%", "", 1)
                per = int(per)
                eta = d["eta"]
                speed = d["_speed_str"]
                size = d["_total_bytes_str"]
                bytesx = d["total_bytes"]
                if str(bytesx) in flex:
                    pass
                else:
                    flex[str(bytesx)] = 1
                if flex[str(bytesx)] == 1:
                    flex[str(bytesx)] += 1
                    try:
                        if eta > 2:
                            lel.edit(
                                f"Downloading {title[:50]}\n\n**FileSize:** {size}\n**Downloaded:** {percentage}\n**Speed:** {speed}\n**ETA:** {eta} sec"
                            )
                    except Exception as e:
                        pass
                if per > 250:
                    if flex[str(bytesx)] == 2:
                        flex[str(bytesx)] += 1
                        if eta > 2:
                            lel.edit(
                                f"**Downloading** {title[:50]}..\n\n**FileSize:** {size}\n**Downloaded:** {percentage}\n**Speed:** {speed}\n**ETA:** {eta} sec"
                            )
                        print(
                            f"[{url_suffix}] Downloaded {percentage} at a speed of {speed} | ETA: {eta} seconds"
                        )
                if per > 500:
                    if flex[str(bytesx)] == 3:
                        flex[str(bytesx)] += 1
                        if eta > 2:
                            lel.edit(
                                f"**Downloading** {title[:50]}...\n\n**FileSize:** {size}\n**Downloaded:** {percentage}\n**Speed:** {speed}\n**ETA:** {eta} sec"
                            )
                        print(
                            f"[{url_suffix}] Downloaded {percentage} at a speed of {speed} | ETA: {eta} seconds"
                        )
                if per > 800:
                    if flex[str(bytesx)] == 4:
                        flex[str(bytesx)] += 1
                        if eta > 2:
                            lel.edit(
                                f"**Downloading** {title[:50]}....\n\n**FileSize:** {size}\n**Downloaded:** {percentage}\n**Speed:** {speed}\n**ETA:** {eta} sec"
                            )
                        print(
                            f"[{url_suffix}] Downloaded {percentage} at a speed of {speed} | ETA: {eta} seconds"
                        )
            if d["status"] == "finished":
                try:
                    taken = d["_elapsed_str"]
                except Exception as e:
                    taken = "00:00"
                size = d["_total_bytes_str"]
                lel.edit(
                    f"**Downloaded** {title[:50]}.....\n\n**FileSize:** {size}\n**Time Taken:** {taken} sec\n\n**Converting File**[__FFmpeg processing__]"
                )
                print(f"[{url_suffix}] Downloaded| Elapsed: {taken} seconds")

        loop = asyncio.get_event_loop()
        x = await loop.run_in_executor(None, youtube.download, url, my_hook)
        file_path = await Codexun.tgcalls.convert(x)
    else:
        if len(message.command) < 2:
            return await lel.edit(
                "**Give me song name !**"
            )
        await lel.edit("**Connected successfully !**")
        query = message.text.split(None, 1)[1]
        # print(query)
        await lel.edit("**Searching your song..**")
        try:
            results = YoutubeSearch(query, max_results=5).to_dict()
            url = f"https://youtube.com{results[0]['url_suffix']}"
            # print results
            title = results[0]["title"][:12]
            thumbnail = results[0]["thumbnails"][0]
            thumb_name = f"thumb{title}.jpg"
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, "wb").write(thumb.content)
            duration = results[0]["duration"]
            url_suffix = results[0]["url_suffix"]
            views = results[0]["views"]
            durl = url
            durl = durl.replace("youtube", "youtubepp")

            secmul, dur, dur_arr = 1, 0, duration.split(":")
            for i in range(len(dur_arr) - 1, -1, -1):
                dur += int(dur_arr[i]) * secmul
                secmul *= 60

        except Exception as e:
            await lel.edit(
                "• **Song not found**\n`write name correctly.`"
            )
            print(str(e))
            return

        keyboard = InlineKeyboardMarkup(
    [
        
       [
            InlineKeyboardButton("03:45----------01:15", callback_data="nothing"),
        ],[
            InlineKeyboardButton("▷", callback_data="resumevc"),
            InlineKeyboardButton("II", callback_data="pausevc"),
            InlineKeyboardButton("‣‣I", callback_data="skipvc"),
            InlineKeyboardButton("▣", callback_data="stopvc"),
        ],[
            InlineKeyboardButton("Menu", callback_data="menu"),
            InlineKeyboardButton("Close", callback_data="cls"),
        ],
        
    ]
)

        if (dur / 60) > DURATION_LIMIT:
            await lel.edit(
                f"💡 Videos longer than {DURATION_LIMIT} minutes aren't allowed to play!"
            )
            return
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail, userid)

        def my_hook(d):
            if d["status"] == "downloading":
                percentage = d["_percent_str"]
                per = (str(percentage)).replace(".", "", 1).replace("%", "", 1)
                per = int(per)
                eta = d["eta"]
                speed = d["_speed_str"]
                size = d["_total_bytes_str"]
                bytesx = d["total_bytes"]
                if str(bytesx) in flex:
                    pass
                else:
                    flex[str(bytesx)] = 1
                if flex[str(bytesx)] == 1:
                    flex[str(bytesx)] += 1
                    try:
                        if eta > 2:
                            lel.edit(
                                f"**Downloading given song**"
                            )
                    except Exception as e:
                        pass
                if per > 250:
                    if flex[str(bytesx)] == 2:
                        flex[str(bytesx)] += 1
                        if eta > 2:
                            lel.edit(
                                f"**Downloading given song..**"
                            )
                        print(
                            f"[{url_suffix}] Downloaded {percentage} at a speed of {speed} | ETA: {eta} seconds"
                        )
                if per > 500:
                    if flex[str(bytesx)] == 3:
                        flex[str(bytesx)] += 1
                        if eta > 2:
                            lel.edit(
                                f"**Downloading given song..**"
                            )
                        print(
                            f"[{url_suffix}] Downloaded {percentage} at a speed of {speed} | ETA: {eta} seconds"
                        )
                if per > 800:
                    if flex[str(bytesx)] == 4:
                        flex[str(bytesx)] += 1
                        if eta > 2:
                            lel.edit(
                                f"**Downloding give song..**"
                            )
                        print(
                            f"[{url_suffix}] Downloaded {percentage} at a speed of {speed} | ETA: {eta} seconds"
                        )
            if d["status"] == "finished":
                try:
                    taken = d["_elapsed_str"]
                except Exception as e:
                    taken = "00:00"
                size = d["_total_bytes_str"]
                lel.edit(
                    f"**Connecting voice chat...**"
                )
                print(f"[{url_suffix}] Downloaded| Elapsed: {taken} seconds")

        loop = asyncio.get_event_loop()
        x = await loop.run_in_executor(None, youtube.download, url, my_hook)
        file_path = await Codexun.tgcalls.convert(x)

    if await is_active_chat(message.chat.id):
        position = await queues.put(message.chat.id, file=file_path)
        await message.reply_photo(
            photo="final.png",
            reply_markup=keyboard,
        )
    else:
        try:
            await calls.pytgcalls.join_group_call(
                message.chat.id,
                InputStream(
                    InputAudioStream(
                        file_path,
                    ),
                ),
                stream_type=StreamType().local_stream,
            )
        except Exception:
            return await lel.edit(
                "**Error ! Make sure Voice Chat is Enabled.**"
            )

        await music_on(message.chat.id)
        await add_active_chat(message.chat.id)
        await message.reply_photo(
            photo="final.png",
            reply_markup=keyboard,
        )

    os.remove("final.png")
    return await lel.delete()
