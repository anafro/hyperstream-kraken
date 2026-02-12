from sqlalchemy.engine import URL, Engine
from sqlalchemy.engine.create import create_engine


class SongMetadataStorage:
    pgsql_engine: Engine

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
