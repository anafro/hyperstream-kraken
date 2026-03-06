from sqlalchemy import Delete, Select, delete
from sqlalchemy.engine import URL, Engine
from sqlalchemy.engine.create import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.sql import select
from sqlalchemy_utils import database_exists, create_database

from hyperstreamkraken.models.base import Base
from hyperstreamkraken.models.song_metadata import SongMetadata


class SongMetadataStorage:
    pgsql_engine: Engine
    DatabaseSession: sessionmaker[Session]

    def __init__(
        self,
        pgsql_host: str,
        pgsql_username: str,
        pgsql_password: str,
        pgsql_database: str,
    ) -> None:
        pgsql_url: URL = URL.create(
            drivername="postgresql+psycopg",
            username=pgsql_username,
            password=pgsql_password,
            host=pgsql_host,
            port=5432,
            database=pgsql_database,
        )
        self.pgsql_engine = create_engine(url=pgsql_url)
        self.DatabaseSession = sessionmaker(
            bind=self.pgsql_engine, expire_on_commit=False
        )
        if not database_exists(self.pgsql_engine.url):
            create_database(self.pgsql_engine.url)
        Base.metadata.create_all(bind=self.pgsql_engine)

    def all(self) -> list[SongMetadata]:
        with self.DatabaseSession() as session:
            statement: Select[tuple[SongMetadata]] = select(SongMetadata).order_by(
                SongMetadata.id.desc()
            )
            return list(session.scalars(statement=statement))

    def store(self, song_metadata: SongMetadata) -> None:
        with self.DatabaseSession() as session:
            session.add(song_metadata)
            session.commit()

    def find(self, id: int) -> SongMetadata | None:
        with self.DatabaseSession() as session:
            return session.get(SongMetadata, ident=id)

    def remove(self, id: int) -> None:
        with self.DatabaseSession() as session:
            statement: Delete = delete(SongMetadata).where(SongMetadata.id == id)
            _ = session.execute(statement)
            session.commit()
