# This file is a part of TG-FileStreamBot
# Coding : Jyothis Jayanth [@EverythingSuckz]

import logging
import re
from pyrogram import filters, errors
from WebStreamer.vars import Var
from urllib.parse import quote_plus
from WebStreamer.bot import StreamBot, logger
from WebStreamer.utils import get_hash, get_name
from pyrogram.enums.parse_mode import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import urllib.parse


def humanbytes(size):
    # https://stackoverflow.com/a/49361727/4723940
    # 2**10 = 1024
    if not size:
        return ""
    power = 2**10
    n = 0
    Dic_powerN = {0: ' ', 1: 'Ki', 2: 'Mi', 3: 'Gi', 4: 'Ti'}
    while size > power:
        size /= power
        n += 1
    return str(round(size, 2)) + " " + Dic_powerN[n] + 'B'

def get_media_file_size(m):
    media = m.video or m.audio or m.document
    if media and media.file_size:
        return media.file_size
    else:
        return None


def get_media_file_name(m):
    media = m.video or m.document or m.audio
    if media and media.file_name:
        return urllib.parse.quote_plus(media.file_name)
    else:
        return None

@StreamBot.on_message(
    filters.private
    & filters.text,
    group=4,
)
async def message_handler(_, m: Message):
    match = re.search("https://t.me/c/(\d+)/(\d+)", m.text)
    if match:
        return await m.reply(f"{Var.URL}{match.group(1)}/{match.group(2)}/")


@StreamBot.on_message(
    filters.private
    & (
        filters.document
        | filters.video
        | filters.audio
        | filters.animation
        | filters.voice
        | filters.video_note
        | filters.photo
        | filters.sticker
    ),
    group=4,
)
async def media_receive_handler(_, m: Message):
    if Var.ALLOWED_USERS and not ((str(m.from_user.id) in Var.ALLOWED_USERS) or (m.from_user.username in Var.ALLOWED_USERS)):
        return await m.reply("You are not <b>allowed to use</b> this <a href='https://github.com/EverythingSuckz/TG-FileStreamBot'>bot</a>.", quote=True)
    #log_msg = await m.forward(chat_id=Var.BIN_CHANNEL, as_copy=True)
    log_msg = await StreamBot.copy_message(Var.BIN_CHANNEL, Var.BOT_UID, m.id)
    file_hash = get_hash(log_msg, Var.HASH_LENGTH)
    #stream_link = f"{Var.URL}{Var.BIN_CHANNEL_ID}/{log_msg.id}/{quote_plus(get_name(m))}?hash={file_hash}"
    stream_link = f"{Var.URL}{Var.BIN_CHANNEL_ID}/{log_msg.id}/{quote_plus(get_name(m))}"
    short_link = f"{Var.URL}{file_hash}{log_msg.id}"
    logger.info(f"Generated link: {stream_link} for {m.from_user.first_name}")
    try:
        media = m.video or m.document or m.audio
        file_name = media.file_name
        file_size = humanbytes(get_media_file_size(m))

        msg_text ="""
<i><u>𝗬𝗼𝘂𝗿 𝗟𝗶𝗻𝗸 𝗚𝗲𝗻𝗲𝗿𝗮𝘁𝗲𝗱 !</u></i>\n
<b>📂 Fɪʟᴇ ɴᴀᴍᴇ :</b> <i>{}</i>\n
<b>📥 Dᴏᴡɴʟᴏᴀᴅ :</b> <i>{}</i>\n
<b>📦 Fɪʟᴇ ꜱɪᴢᴇ :</b> <i>{}</i>\n"""
        #await log_msg.reply_text(text=f"**RᴇQᴜᴇꜱᴛᴇᴅ ʙʏ :** [{m.from_user.first_name}](tg://user?id={m.from_user.id})\n**Uꜱᴇʀ ɪᴅ :** `{m.from_user.id}`\n**Dᴏᴡɴʟᴏᴀᴅ ʟɪɴᴋ :** {stream_link}", disable_web_page_preview=True, parse_mode=ParseMode.MARKDOWN, quote=True)

        await m.reply_text(
            #text="<code>{}</code>\n(<a href='{}'>shortened</a>)".format(
            #    stream_link, short_link
            #),
            text=msg_text.format(file_name, stream_link, file_size),
            quote=True,
            parse_mode=ParseMode.HTML,
            #reply_markup=InlineKeyboardMarkup(
            #    [[InlineKeyboardButton("Open", url=stream_link)]]
            #),
        )
    except errors.ButtonUrlInvalid:
        await m.reply_text(
            text="<code>{}</code>\n\nshortened: {})".format(
                stream_link, short_link
            ),
            quote=True,
            parse_mode=ParseMode.HTML,
        )
