from typing import Any, override
from bourgade import Event


class SongFoundEvent(Event):
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
        )

    @override
    def set_content_from_dict(self, content: dict[str, Any]) -> None:
        self.id = content["id"]
        self.author = content["author"]
        self.title = content["title"]
        self.length = content["length"]

    @staticmethod
    @override
    def get_event_name() -> str:
        return "song.found"
