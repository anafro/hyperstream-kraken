from dataclasses import dataclass
from datetime import timedelta
from typing import override
from bourgade import EventBus, EventHandler

from hyperstreamkraken.messaging.song_find_event import SongFindEvent
from hyperstreamkraken.messaging.song_found_event import SongFoundEvent
from hyperstreamkraken.models.song_metadata import SongMetadata
from hyperstreamkraken.storage.song_storage import SongStorage


@dataclass(frozen=True)
class SongFindEventHandler(EventHandler[SongFindEvent]):
    song_storage: SongStorage
    event_bus: EventBus

    @override
    async def handle(self, event: SongFindEvent) -> None:
        song: SongMetadata | None = self.song_storage.metadatas.find(event.id)

        await self.event_bus.dispatch(
            SongFoundEvent.create(
                event_bus=self.event_bus,
                content=dict(**(song.to_dict() if song is not None else {})),
            ),
        )
