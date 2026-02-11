from typing import override
from hyperstreamkraken.messaging.song_download_requested_event import (
    SongDownloadRequestedEvent,
)
from hyperstreamkraken.messaging.rabbitmq_event_bus import RabbitMQEventHandler
from hyperstreamkraken.downloading.pytubefix_downloader import PytubefixDownloader
from hyperstreamkraken.downloading.song_downloader import SongDownloader
from hyperstreamkraken.metadata.song import Song


class SongDownloadRequestedEventHandler(
    RabbitMQEventHandler[SongDownloadRequestedEvent]
):
    song_downloader: SongDownloader

    def __init__(self) -> None:
        super().__init__(self)
        self.song_downloader = PytubefixDownloader()

    @override
    def handle(self, event: SongDownloadRequestedEvent) -> None:
        song_query: str = event.query
        song: Song = self.song_downloader.download_song(song_query=song_query)
        # TODO:  Upload to S3
        # TODO:  Fire events
