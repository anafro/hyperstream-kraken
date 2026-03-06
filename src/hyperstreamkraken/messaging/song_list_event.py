from typing import Any, override
from bourgade import Event


class SongListEvent(Event):
    query: str

    @override
    def set_content_from_dict(self, content: dict[str, Any]) -> None:
        pass

    @override
    def get_content_as_dict(self) -> dict[str, Any]:
        return {}

    @override
    @staticmethod
    def get_event_name() -> str:
        return "song.list"
