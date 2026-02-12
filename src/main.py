import logging
from argparse import ArgumentParser, Namespace
from sys import argv

from hyperstreamkraken.cli import CLIArgs
from hyperstreamkraken.downloading.pytubefix_downloader import PytubefixDownloader
from hyperstreamkraken.downloading.song_downloader import SongDownloader
from hyperstreamkraken.messaging.rabbitmq_event import RabbitMQEventBus
from hyperstreamkraken.messaging.song_download_requested_event_handler import (
    SongDownloadRequestedEventHandler,
)
from hyperstreamkraken.models.song import Song
from hyperstreamkraken.utils.secrets import get_secret
from hyperstreamkraken.storage.song_storage import SongStorage

logger: logging.Logger = logging.Logger(__name__)


def main() -> None:
    downloader = PytubefixDownloader()
    if len(argv) == 1:
        run_as_microservice(downloader)
    else:
        run_as_cli(downloader)


def run_as_microservice(downloader: SongDownloader) -> None:
    rabbitmq_host: str = get_secret("RABBITMQ_HOST")
    rabbitmq_username: str = get_secret("RABBITMQ_USER")
    rabbitmq_password: str = get_secret("RABBITMQ_PASS")
    rabbitmq_exchange_name: str = get_secret("RABBITMQ_EXCHANGE")

    event_bus = RabbitMQEventBus(
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
    song_storage: SongStorage = SongStorage(
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

    event_bus.register_handler(
        SongDownloadRequestedEventHandler(
            song_downloader=downloader, song_storage=song_storage
        )
    )

    event_bus.start_listening()


def run_as_cli(downloader: SongDownloader) -> None:
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
        main()
    except KeyboardInterrupt:
        logger.warning("Ctrl+C'd! Goodbye")
    except Exception as exception:
        logger.critical(msg="Unexpected exception occurred", exc_info=exception)
