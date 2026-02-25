from typing import Any, override
from typing import cast
from bourgade import Event
import json


class SongDownloadRequestedEvent(Event):
    query: str

    @override
    def hydrate(self) -> None:
        payload: dict[str, Any] = self.json()
        self.query = cast(str, payload.get("query"))

    @override
    def serialize(self) -> bytes:
        return json.dumps({"query": self.query}).encode("utf-8")

    @override
    @staticmethod
    def get_event_name() -> str:
        return "song.download.requested"
