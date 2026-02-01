import logging
from yt_dlp import YoutubeDL
from typing import override
from hyperstreamkraken.downloading.song_downloader import SongDownloader
from hyperstreamkraken.metadata.song import Song
import urllib.parse


class YtdlpDownloader(SongDownloader):
    @override
    def download_song(self, song_query: str) -> Song:
        yt_dlp_options = {
            "format": "bestaudio/best",
            "outtmpl": "/tmp/%(id)s.%(ext)s",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                }
            ],
            "extractor_args": {"youtube": {"player_client": ["tv"]}},
            "noplaylist": True,
            "quiet": False,
            "logger": logging.getLogger(),
        }

        query = urllib.parse.quote_plus(song_query)
        search_url = f"https://www.youtube.com/results?search_query={query}"

        with YoutubeDL(yt_dlp_options) as ydl:
            info = ydl.extract_info(search_url, download=False)
            entries = info.get("entries") or []
            if not entries:
                raise RuntimeError(f"No YouTube results for '{song_query}'")
            video_info = entries[0]
            ydl.download([video_info.get("webpage_url")])

        mp3_path = f"/tmp/{video_info['id']}.mp3"
        with open(mp3_path, "rb") as f:
            audio_bytes = f.read()

        return Song(
            title=video_info.get("title"),
            author=video_info.get("uploader"),
            audio_buffer=audio_bytes,
        )
