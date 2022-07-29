from os import getenv
from dotenv import load_dotenv

# .env読み込み
load_dotenv()

# DiscordのBotトークン(アプリケーション発行時に取得したもの)
DISCORD_TOKEN = getenv("DISCORD_TOKEN")
# 読み上げ対象のチャンネルID
DISCORD_CHANNEL_TEXT_ID = int(getenv("DISCORD_CHANNEL_TEXT_ID"))
DISCORD_CHANNEL_VOICE_ID = int(getenv("DISCORD_CHANNEL_VOICE_ID"))

# 読み上げ最小必要文字数
TTS_MIN_TEXT_LENGTH = int(getenv("TTS_MIN_TEXT_LENGTH"))
# 読み上げ最大対応文字数
TTS_MAX_TEXT_LENGTH = int(getenv("TTS_MAX_TEXT_LENGTH"))

# VVの各種エンドポイント(基本的に変更は必要無いはずなので固定値)
VV_ENDPOINT_QUERY = "http://127.0.0.1:50031/audio_query"
VV_ENDPOINT_SPEAKER = "http://127.0.0.1:50031/speakers"
VV_ENDPOINT_AUDIO = "http://127.0.0.1:50031/synthesis"
