from io import BytesIO
import subprocess
from typing import override

from pytubefix import Stream, YouTube
from pytubefix.cli import on_progress

from hyperstreamkraken.downloading.song_downloader import SongDownloader
from hyperstreamkraken.metadata.song import Song
from hyperstreamkraken.youtube.youtube_search import search_youtube_video_link


class PytubefixDownloader(SongDownloader):
    @override
    def download_song(self, song_query: str) -> Song:
        youtube_link = search_youtube_video_link(song_query)
        pytubefix: YouTube = YouTube(youtube_link, on_progress_callback=on_progress)

        audio_stream: Stream | None = pytubefix.streams.get_audio_only()

        if audio_stream is None:
            raise ValueError(
                f"Can't download audio '{song_query}' by link '{youtube_link}'."
            )

        m4a_buffer = BytesIO()
        audio_stream.stream_to_buffer(m4a_buffer)
        _ = m4a_buffer.seek(0)

        mp3_process = subprocess.Popen(
            [
                "ffmpeg",
                "-i",
                "pipe:0",
                "-f",
                "mp3",
                "-codec:a",
                "libmp3lame",
                "-b:a",
                "192k",
                "pipe:1",
            ],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )

        audio_bytes, _ = mp3_process.communicate(m4a_buffer.read())

        return Song(
            title=pytubefix.title,
            author=pytubefix.author,
            audio_buffer=audio_bytes,
        )
