from dataclasses import dataclass
from typing import override
from hyperstreamkraken.messaging.rabbitmq_event import RabbitMQEventHandler
from hyperstreamkraken.messaging.song_download_requested_event import (
    SongDownloadRequestedEvent,
)
from hyperstreamkraken.downloading.song_downloader import SongDownloader
from hyperstreamkraken.models.song import Song
from hyperstreamkraken.storage.song_storage import SongStorage


@dataclass(frozen=True)
class SongDownloadRequestedEventHandler(
    RabbitMQEventHandler[SongDownloadRequestedEvent]
):
    song_downloader: SongDownloader
    song_storage: SongStorage

    @override
    def handle(self, event: SongDownloadRequestedEvent) -> None:
        song_query: str = event.query
        song: Song = self.song_downloader.download_song(song_query=song_query)
        self.song_storage.store(song)
