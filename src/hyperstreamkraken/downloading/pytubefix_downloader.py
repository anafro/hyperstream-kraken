from io import BytesIO
import subprocess
from typing import override

from pytubefix import Stream, YouTube  # pyright: ignore[reportMissingTypeStubs]
from pytubefix.cli import on_progress  # pyright: ignore[reportMissingTypeStubs]

from hyperstreamkraken.downloading.song_downloader import SongDownloader
from hyperstreamkraken.models.song import Song
from hyperstreamkraken.models.song_metadata import SongMetadata, SongSources
from hyperstreamkraken.youtube.youtube_search import YoutubeSearch, search_on_youtube


class PytubefixDownloader(SongDownloader):
    @override
    def download_song(self, song_query: str) -> Song:
        search_result: YoutubeSearch = search_on_youtube(song_query)

        pytubefix: YouTube = YouTube(
            search_result.url, on_progress_callback=on_progress
        )

        audio_stream: Stream | None = pytubefix.streams.get_audio_only()

        if audio_stream is None:
            raise ValueError(
                f"Can't download audio '{song_query}' by link '{search_result.url}'."
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
            metadata=SongMetadata(
                source_id=SongSources.YOUTUBE.value.id,
                id_from_source=search_result.id,
                title=pytubefix.title,
                author=pytubefix.author,
            ),
            audio_buffer=audio_bytes,
        )
