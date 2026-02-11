import logging
from argparse import ArgumentParser, Namespace
from sys import argv

from hyperstreamkraken.cli import CLIArgs
from hyperstreamkraken.downloading.pytubefix_downloader import PytubefixDownloader
from hyperstreamkraken.downloading.song_downloader import SongDownloader
from hyperstreamkraken.metadata.song import Song

logger: logging.Logger = logging.Logger(__name__)


def main() -> None:
    downloader = PytubefixDownloader()
    if len(argv) == 1:
        run_as_microservice(downloader)
    else:
        run_as_cli(downloader)


def run_as_microservice(downloader: SongDownloader) -> None:
    raise NotImplementedError()


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
