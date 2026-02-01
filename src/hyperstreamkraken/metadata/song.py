from dataclasses import dataclass


@dataclass(frozen=True)
class Song:
    title: str
    author: str
    audio_buffer: bytes

    def to_mp3_file(self, path: str) -> None:
        with open(path, "wb") as mp3_file:
            _ = mp3_file.write(self.audio_buffer)
