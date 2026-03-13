from dataclasses import dataclass
from datetime import timedelta
from typing import override
from bourgade import EventBus, EventHandler

from hyperstreamkraken.messaging.song_expose_event import SongExposeEvent
from hyperstreamkraken.messaging.song_exposed_event import SongExposedEvent
from hyperstreamkraken.models.song_metadata import SongMetadata
from hyperstreamkraken.storage.song_storage import SongStorage


@dataclass(frozen=True)
class SongExposeEventHandler(EventHandler[SongExposeEvent]):
    song_storage: SongStorage
    event_bus: EventBus

    @override
    async def handle(self, event: SongExposeEvent) -> None:
        uri: str = self.song_storage.files.presign_s3_uri(
            song_id=event.id,
            expires_in=timedelta(minutes=5),
            external=event.sid is not None,
        )
        song: SongMetadata | None = self.song_storage.metadatas.find(event.id)

        await self.event_bus.dispatch(
            SongExposedEvent.create(
                event_bus=self.event_bus,
                content=dict(uri=uri, **(song.to_dict() if song is not None else {})),
            ),
        )
