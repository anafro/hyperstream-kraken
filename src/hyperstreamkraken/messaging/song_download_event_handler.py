from dataclasses import dataclass
from typing import override

from bourgade import EventBus, EventHandler
from hyperstreamkraken.downloading.song_downloader import SongDownloader
from hyperstreamkraken.messaging.song_download_event import SongDownloadEvent
from hyperstreamkraken.messaging.song_download_fail_event import SongDownloadFailEvent
from hyperstreamkraken.messaging.song_downloaded_event import SongDownloadedEvent
from hyperstreamkraken.models.song import Song
from hyperstreamkraken.storage.song_storage import SongStorage


@dataclass(frozen=True)
class SongDownloadEventHandler(EventHandler[SongDownloadEvent]):
    song_downloader: SongDownloader
    song_storage: SongStorage
    event_bus: EventBus

    @override
    async def handle(self, event: SongDownloadEvent) -> None:
        song_query: str = event.query
        try:
            song: Song = self.song_downloader.download_song(song_query=song_query)
            self.song_storage.store(song)
            await self.event_bus.dispatch(
                SongDownloadedEvent.create(
                    self.event_bus, content=song.metadata.to_dict()
                )
            )
        except Exception as exception:
            await self.event_bus.dispatch(
                SongDownloadFailEvent.create(
                    event_bus=self.event_bus,
                    content=dict(message=str(exception)),
                )
            )
