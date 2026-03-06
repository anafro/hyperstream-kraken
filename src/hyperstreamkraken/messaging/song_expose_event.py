from typing import Any, override
from bourgade import Event


class SongExposeEvent(Event):
    id: int

    @override
    def get_content_as_dict(self) -> dict[str, Any]:
        return dict(id=self.id)

    @override
    def set_content_from_dict(self, content: dict[str, Any]) -> None:
        self.id = content["id"]

    @staticmethod
    @override
    def get_event_name() -> str:
        return "song.expose"
