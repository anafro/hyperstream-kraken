from typing import Any, override
from bourgade import Event


class SongExposedEvent(Event):
    id: int
    author: str
    title: str
    length: int
    uri: str

    @override
    def get_content_as_dict(self) -> dict[str, Any]:
        return dict(
            id=self.id,
            author=self.author,
            title=self.title,
            length=self.length,
            uri=self.uri,
        )

    @override
    def set_content_from_dict(self, content: dict[str, Any]) -> None:
        self.id = content["id"]
        self.author = content["author"]
        self.title = content["title"]
        self.length = content["length"]
        self.uri = content["uri"]

    @staticmethod
    @override
    def get_event_name() -> str:
        return "song.exposed"
