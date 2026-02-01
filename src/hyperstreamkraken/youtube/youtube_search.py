import urllib.parse
import logging
from yt_dlp import YoutubeDL
from yt_dlp import YoutubeDL
import logging


def search_youtube_video_link(query: str) -> str:
    search_query = f"ytsearch:{query}"

    yt_dlp_options = {
        "format": "bestaudio/best",
        "noplaylist": True,
        "quiet": True,
        "logger": logging.getLogger(),
    }

    with YoutubeDL(yt_dlp_options) as ydl:
        info = ydl.extract_info(search_query, download=False)
        entries = info.get("entries") or []
        if not entries:
            raise RuntimeError(f"No YouTube results for '{query}'")
        video_info = entries[0]
        return video_info.get("webpage_url")
