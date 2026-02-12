from abc import ABC, abstractmethod

from hyperstreamkraken.models.song import Song


class SongDownloader(ABC):
    @abstractmethod
    def download_song(self, song_query: str) -> Song: ...
