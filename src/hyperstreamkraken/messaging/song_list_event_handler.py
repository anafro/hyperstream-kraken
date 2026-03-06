from typing import override
from bourgade import EventBus, EventHandler, dataclass
from hyperstreamkraken.messaging.song_list_event import SongListEvent
from hyperstreamkraken.messaging.song_listed_event import SongListedEvent
from hyperstreamkraken.storage.song_storage import SongStorage


@dataclass(frozen=True)
class SongListEventHandler(EventHandler[SongListEvent]):
    song_storage: SongStorage
    event_bus: EventBus

    @override
    async def handle(self, event: SongListEvent) -> None:
        await self.event_bus.dispatch(
            SongListedEvent.create(
                self.event_bus,
                {
                    "songs": [
                        song.to_dict() for song in self.song_storage.metadatas.all()
                    ],
                },
            )
        )
