from abc import ABC
from typing import Any, override
from bourgade import Event


class FailEvent(Event, ABC):
    message: str

    @override
    def set_content_from_dict(self, content: dict[str, Any]) -> None:
        self.message = content["message"]

    @override
    def get_content_as_dict(self) -> dict[str, Any]:
        return dict(
            message=self.message,
        )
