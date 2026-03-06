from typing import final
from sqlalchemy import Integer, String
from sqlalchemy.orm import MappedColumn, mapped_column
from hyperstreamkraken.models.base import Base


@final
class SongMetadata(Base):
    __tablename__ = "songs"
    id: MappedColumn[Integer] = mapped_column(Integer, primary_key=True)
    title: MappedColumn[String] = mapped_column(String, nullable=False)
    author: MappedColumn[String] = mapped_column(String, nullable=False)
    length: MappedColumn[Integer] = mapped_column(Integer, nullable=False)
