from typing import Any, override
from bourgade import Event


class SongDownloadEvent(Event):
    query: str

    @override
    def set_content_from_dict(self, content: dict[str, Any]) -> None:
        self.query = content["query"]

    @override
    def get_content_as_dict(self) -> dict[str, Any]:
        return dict(query=self.query)

    @override
    @staticmethod
    def get_event_name() -> str:
        return "song.download"
