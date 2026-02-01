from hyperstreamkraken.downloading.pytubefix_downloader import PytubefixDownloader
from hyperstreamkraken.metadata.song import Song
from sys import argv


def main() -> None:
    downloader = PytubefixDownloader()
    song_name = " ".join(argv[1:])
    print("Downloading the song: " + song_name)
    song: Song = downloader.download_song(song_name)
    song.to_mp3_file("/home/anafro/kraken-download.mp3")


if __name__ == "__main__":
    main()
