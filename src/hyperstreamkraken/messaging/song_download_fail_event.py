from typing import Any, override

from hyperstreamkraken.utils.messaging.fail_event import FailEvent


class SongDownloadFailEvent(FailEvent):
    @staticmethod
    @override
    def get_event_name() -> str:
        return "song.download.fail"
