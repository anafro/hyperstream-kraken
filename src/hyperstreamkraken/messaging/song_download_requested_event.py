from typing import Any, override
from hyperstreamkraken.messaging.rabbitmq_event import RabbitMQEvent
from typing import cast
import json


class SongDownloadRequestedEvent(RabbitMQEvent):
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
