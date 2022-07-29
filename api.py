from config import (
    VV_ENDPOINT_SPEAKER,
    VV_ENDPOINT_QUERY,
    VV_ENDPOINT_AUDIO,
)
from typing import Any, Dict, List
import aiohttp


async def get_speaker_list() -> List[int]:
    """VVのAPIから現在対応しているスピーカーリストを取得します

    Returns:
        List[int]: スピーカーID一覧
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(VV_ENDPOINT_SPEAKER) as resp:
            return [j["styles"][0]["id"] for j in await resp.json()]


async def __get_text_query(
    speaker_id: int, text: str
) -> Dict[str, Any]:
    """VVのAPIにて テキストからクエリを取得します

    Args:
        speaker_id (int): 話者ID
        text (str): 読み上げるテキスト

    Returns:
        Dict[str,Any] : アクセントデータ
    """
    REQUEST_PARAMS = {
        "text": text,
        "speaker": str(speaker_id),
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(
            VV_ENDPOINT_QUERY,
            params=REQUEST_PARAMS
        ) as resp:
            return await resp.json()


async def get_speaking_wave(speaker_id: int, text: str) -> bytes:
    """VVのAPIにて テキストを音声に変換します

    Args:
        speaker_id (int): 話者ID
        text (str): 読み上げるテキスト

    Returns:
        bytes: 音声データ
    """
    queries = await __get_text_query(speaker_id, text)
    # テキストからアクセントを取得
    REQUEST_PARAMS = {
        "text": text,
        "speaker": str(speaker_id),
        "enable_interrogative_upspeak": "false",
    }
    REQUEST_JSON = queries
    async with aiohttp.ClientSession() as session:
        async with session.post(
            VV_ENDPOINT_AUDIO,
            params=REQUEST_PARAMS,
            json=REQUEST_JSON
        ) as resp:
            return await resp.read()
