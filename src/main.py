import asyncio
import logging
from argparse import ArgumentParser, Namespace
from sys import argv

from shhh import get_secret
from bourgade import EventBus

from hyperstreamkraken.api.http import (
    start_http_api_server_daemon,
)
from hyperstreamkraken.cli import CLIArgs
from hyperstreamkraken.downloading.pytubefix_downloader import PytubefixDownloader
from hyperstreamkraken.downloading.song_downloader import SongDownloader
from hyperstreamkraken.messaging.song_download_event_handler import (
    SongDownloadEventHandler,
)
from hyperstreamkraken.messaging.song_expose_event_handler import SongExposeEventHandler
from hyperstreamkraken.messaging.song_list_event_handler import SongListEventHandler
from hyperstreamkraken.models.song import Song
from hyperstreamkraken.models.song_metadata import SongMetadata
from hyperstreamkraken.storage.song_storage import SongStorage

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger: logging.Logger = logging.getLogger(__name__)


async def on_progress_in_cli(
    song_metadata: SongMetadata, progress_percent: float
) -> None:
    logger.info(
        "[{}%] Downloading {} - {} [{}]...",
        song_metadata.author,
        song_metadata.title,
        song_metadata.length,
        progress_percent,
    )


async def main() -> None:
    if len(argv) == 1:
        await run_as_microservice()
    else:
        await run_as_cli()


async def run_as_microservice() -> None:
    logger.info("Kraken service is starting up")

    rabbitmq_host: str = get_secret("RABBITMQ_HOST")
    rabbitmq_username: str = get_secret("RABBITMQ_USER")
    rabbitmq_password: str = get_secret("RABBITMQ_PASS")
    rabbitmq_exchange_name: str = get_secret("RABBITMQ_EXCHANGE")

    event_bus: EventBus = await EventBus.create(
        host=rabbitmq_host,
        username=rabbitmq_username,
        password=rabbitmq_password,
        exchange_name=rabbitmq_exchange_name,
        queue_name="kraken.v1",
    )

    s3_host: str = get_secret("S3_HOST")
    s3_access_key: str = get_secret("S3_ACCESS_KEY")
    s3_secret_key: str = get_secret("S3_SECRET_KEY")
    s3_region: str = get_secret("S3_REGION")
    s3_bucket: str = get_secret("S3_BUCKET")
    pgsql_host: str = get_secret("PGSQL_HOST")
    pgsql_username: str = get_secret("PGSQL_USERNAME")
    pgsql_password: str = get_secret("PGSQL_PASSWORD")
    pgsql_database: str = get_secret("PGSQL_DATABASE")
    songs: SongStorage = SongStorage(
        s3_host=s3_host,
        s3_access_key=s3_access_key,
        s3_secret_key=s3_secret_key,
        s3_bucket=s3_bucket,
        s3_region=s3_region,
        pgsql_host=pgsql_host,
        pgsql_username=pgsql_username,
        pgsql_password=pgsql_password,
        pgsql_database=pgsql_database,
    )

    downloader: SongDownloader = PytubefixDownloader()

    event_bus.register_handler(
        SongDownloadEventHandler(
            song_downloader=downloader, song_storage=songs, event_bus=event_bus
        )
    )

    event_bus.register_handler(
        SongListEventHandler(
            song_storage=songs,
            event_bus=event_bus,
        )
    )

    event_bus.register_handler(
        SongExposeEventHandler(song_storage=songs, event_bus=event_bus)
    )

    start_http_api_server_daemon(port=44099, songs=songs)
    await event_bus.start_listening()


async def run_as_cli() -> None:
    downloader: SongDownloader = PytubefixDownloader()

    arg_parser: ArgumentParser = ArgumentParser(
        prog="HyperstreamKraken", description="Downloads songs by a query to a file"
    )
    _ = arg_parser.add_argument(
        "-q", "--query", type=str, help="A song query you want to download"
    )
    _ = arg_parser.add_argument(
        "-o", "--output", type=str, help="A filepath to safe downloaded song to"
    )

    untyped_args: Namespace = arg_parser.parse_args()
    args: CLIArgs = CLIArgs(**vars(untyped_args))

    song: Song = downloader.download_song(args.query)
    song.to_mp3_file(path=args.output)


if __name__ == "__main__":
    try:
        asyncio.run(main=main())
    except KeyboardInterrupt:
        logger.warning("Ctrl+C'd! Goodbye")
    except Exception as exception:
        logger.critical(msg="Unexpected exception occurred", exc_info=exception)
