from hyperstreamkraken.models.song_metadata import SongMetadata
from hyperstreamkraken.storage.song_files_storage import SongFilesStorage
from hyperstreamkraken.models.song import Song
from hyperstreamkraken.storage.song_metadata_storage import SongMetadataStorage


class SongStorage:
    files: SongFilesStorage
    metadatas: SongMetadataStorage
    bucket: str

    def __init__(
        self,
        *,
        s3_host: str,
        s3_access_key: str,
        s3_secret_key: str,
        s3_bucket: str,
        s3_region: str,
        pgsql_host: str,
        pgsql_username: str,
        pgsql_password: str,
        pgsql_database: str,
    ) -> None:
        self.bucket = s3_bucket
        self.files = SongFilesStorage(
            s3_host=s3_host,
            access_key=s3_access_key,
            secret_key=s3_secret_key,
            bucket=s3_bucket,
            region=s3_region,
        )
        self.metadatas = SongMetadataStorage(
            pgsql_host=pgsql_host,
            pgsql_username=pgsql_username,
            pgsql_password=pgsql_password,
            pgsql_database=pgsql_database,
        )

    def store(self, song: Song) -> None:
        pass

    def remove(self, song_id: Song) -> None:
        pass

    def search(
        self, query: str, *, limit: int | None = None, offset: int | None = None
    ) -> SongMetadata:
        return NotImplemented
