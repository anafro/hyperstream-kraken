from dataclasses import dataclass
from pathlib import Path

from hyperstreamkraken.models.song_metadata import SongMetadata


@dataclass(frozen=True)
class Song:
    metadata: SongMetadata
    audio_buffer: bytes

    def to_mp3_file(self, path: Path | str) -> None:
        with open(path, "wb") as mp3_file:
            _ = mp3_file.write(self.audio_buffer)
