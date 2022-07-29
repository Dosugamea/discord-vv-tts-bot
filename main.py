from typing import Any
from config import (
    DISCORD_TOKEN, DISCORD_CHANNEL_TEXT_ID, DISCORD_CHANNEL_VOICE_ID,
    TTS_MAX_TEXT_LENGTH, TTS_MIN_TEXT_LENGTH
)
from api import get_speaker_list, get_speaking_wave
from discord.ext import commands
from mix import MixAudioSource
import uuid
import discord
import re
import os
import asyncio
import datetime

"""
Discord TTS Bot for Modified VV
"""

# Botの初期化処理
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
source = MixAudioSource()
loop = asyncio.get_event_loop()
voices = loop.run_until_complete(get_speaker_list())


@bot.event
async def on_ready():
    """Bot起動時に呼ばれるイベント"""
    c: discord.VoiceClient = await bot.get_channel(
        DISCORD_CHANNEL_VOICE_ID
    ).connect()
    c.play(source)
    print("Ready!")


def is_readable_text(message: Any) -> bool:
    """読み上げるべきテキストかどうかを判定する"""
    if message.author.bot:
        return False
    if message.channel.id != DISCORD_CHANNEL_TEXT_ID:
        return False
    if not message.clean_content:
        return False
    if len(message.clean_content) < TTS_MIN_TEXT_LENGTH:
        return False
    if len(message.clean_content) > TTS_MAX_TEXT_LENGTH:
        return False
    return True


def clean_text(content: str) -> str:
    """読み上げるテキストを整形する"""
    # 絵文字除去
    content = re.sub(r"<a?:([a-zA-Z_]+):\d+>", r"\1", content)
    # URL除去(置き換え)
    content = re.sub(r"https?://[^\s]+", r"URL", content)
    # コード除去
    content = re.sub(r"```[\s\S]*```", r"コード", content)
    return re.sub(r"[\n\r]", "", content)


@bot.event
async def on_message(message: Any) -> None:
    """メッセージを受信したときに呼ばれるイベント"""
    if not is_readable_text(message):
        return
    text = clean_text(message.clean_content)
    speaker = voices[0]
    print(f"{message.author} : {speaker}")
    voice_bytes = await get_speaking_wave(speaker, text)
    id = str(uuid.uuid4())
    with open(f"./voice/{id}.wav", "wb") as f:
        f.write(voice_bytes)
    source.sources.append(
        discord.FFmpegPCMAudio(f"./voice/{id}.wav")
    )
    files = os.listdir("voice")
    for f in files:
        if f.endswith(".wav"):
            created_time = datetime.datetime.fromtimestamp(
                os.stat(os.path.join("voice", f)).st_mtime
            )
            limit_dt = datetime.datetime.now() - datetime.timedelta(minutes=1)
            if created_time < limit_dt:
                os.remove(os.path.join("voice", f))


bot.run(DISCORD_TOKEN)
