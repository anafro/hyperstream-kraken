from typing import Any, cast, override
from bourgade import Event

from hyperstreamkraken.models.song_metadata import SongMetadata


class SongListedEvent(Event):
    songs: list[SongMetadata]

    @override
    def set_content_from_dict(self, content: dict[str, Any]) -> None:
        self.songs = cast(list[SongMetadata], content["songs"])

    @override
    def get_content_as_dict(self) -> dict[str, Any]:
        return dict(songs=self.songs)

    @override
    @staticmethod
    def get_event_name() -> str:
        return "song.listed"
