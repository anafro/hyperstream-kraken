from typing import Any, override

from bourgade import Event


class SongDownloadedEvent(Event):
    id: int
    title: str
    author: str
    length: int

    @override
    def set_content_from_dict(self, content: dict[str, str | int]) -> None:
        self.id = int(content["id"])
        self.title = str(content["title"])
        self.author = str(content["author"])
        self.length = int(content["length"])

    @override
    def get_content_as_dict(self) -> dict[str, Any]:
        return dict(
            id=self.id,
            title=self.title,
            author=self.author,
            length=self.length,
        )

    @staticmethod
    @override
    def get_event_name() -> str:
        return "song.downloaded"
