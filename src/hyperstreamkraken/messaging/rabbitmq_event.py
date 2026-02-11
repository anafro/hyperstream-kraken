from abc import ABC, abstractmethod
from pika.spec import Basic
from typing import Any
import json


class RabbitMQEvent(ABC):
    deliver: Basic.Deliver
    message: bytes

    def __init__(self, deliver: Basic.Deliver, message: bytes) -> None:
        self.deliver = deliver
        self.message = message

    @abstractmethod
    def hydrate(self) -> None: ...

    @abstractmethod
    def serialize(self) -> bytes: ...

    @abstractmethod
    @staticmethod
    def get_event_name() -> str: ...

    def string(self) -> str:
        return self.message.decode(encoding="utf-8")

    def json(self) -> dict[str, Any]:
        return json.loads(self.string())
