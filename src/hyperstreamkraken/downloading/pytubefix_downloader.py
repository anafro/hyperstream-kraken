import logging
from typing import override

from pytubefix import YouTube  # pyright: ignore[reportMissingTypeStubs]

from hyperstreamkraken.downloading.song_downloader import SongDownloader
from hyperstreamkraken.models.song import Song
from hyperstreamkraken.models.song_metadata import SongMetadata
from hyperstreamkraken.utils.pytubefix.audio_buffering import buffer_audio
from hyperstreamkraken.youtube.youtube_search import YoutubeSearch, search_on_youtube

logger: logging.Logger = logging.getLogger(__name__)


class PytubefixDownloader(SongDownloader):
    @override
    def download_song(self, song_query: str) -> Song:
        search_result: YoutubeSearch = search_on_youtube(song_query)
        song_video: YouTube = YouTube(search_result.url)

        song_metadata: SongMetadata = SongMetadata(
            title=song_video.title,
            author=song_video.author,
            length=song_video.length,
        )

        audio_bytes: bytes = buffer_audio(video=song_video)

        return Song(
            metadata=song_metadata,
            audio_buffer=audio_bytes,
        )
