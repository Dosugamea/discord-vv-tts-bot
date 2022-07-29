from os import getenv
import re
import discord
from discord.ext import commands
import aiohttp
import hashlib
import os
from dotenv import load_dotenv

from mix import MixAudioSource

load_dotenv()

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
source = MixAudioSource()
voices = []


@bot.event
async def on_ready():
    global voices
    print("Ready")
    c: discord.VoiceClient = await bot.get_channel(826084795720794129).connect()
    c.play(source)
    async with aiohttp.ClientSession() as session:
        async with session.get(
            "https://api.su-shiki.com/v2/voicevox/speakers/",
            params={"key": getenv("VV_API_KEY")},
        ) as resp:
            voices = [j["styles"][0]["id"] for j in await resp.json()]


@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if message.channel.id != 864436944275374080:
        return
    if not message.clean_content:
        return
    speaker = message.author.id % len(voices)
    print(f"{message.author} : {speaker}")
    content = message.clean_content
    content = re.sub(r"<a?:([a-zA-Z_]+):\d+>", r"\1", content)
    content = re.sub(r"https?://[^\s]+", r"URL", content)
    content = re.sub(r"```[\s\S]*```", r"コード", content)
    txt_hash = hashlib.sha256(f"{content}-{speaker}".encode("utf-8")).hexdigest()
    if not os.path.exists(f"voice/{txt_hash}.wav"):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://api.su-shiki.com/v2/voicevox/audio",
                params={
                    "text": content,
                    "key": getenv("VV_API_KEY"),
                    "speaker": voices[speaker],
                    "enable_interrogative_upspeak": "true",
                },
            ) as resp:
                with open(f"voice/{txt_hash}.wav", "wb") as f:
                    f.write(await resp.read())

    source.sources.append(discord.FFmpegPCMAudio(f"voice/{txt_hash}.wav"))


bot.run(getenv("TOKEN"))
