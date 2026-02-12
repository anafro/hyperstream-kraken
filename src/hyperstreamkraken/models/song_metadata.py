from dataclasses import dataclass
from enum import Enum
from typing import final

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from hyperstreamkraken.models.base import Base


@final
@dataclass
class SongSource(Base):
    __tablename__ = "song_sources"
    name: Mapped[str]
    id: Mapped[int] = mapped_column(primary_key=True)
    songs: Mapped[list["SongMetadata"]] = relationship(back_populates="source")


class SongSources(Enum):
    YOUTUBE = SongSource(id=1, name="YouTube")


@final
@dataclass
class SongMetadata(Base):
    __tablename__ = "songs"
    title: Mapped[str]
    author: Mapped[str]
    source: Mapped["SongSource"] = relationship(back_populates="songs")
    source_id: Mapped[int] = mapped_column(
        ForeignKey("song_sources.id"), primary_key=True
    )
    id_from_source: Mapped[str] = mapped_column(primary_key=True)
