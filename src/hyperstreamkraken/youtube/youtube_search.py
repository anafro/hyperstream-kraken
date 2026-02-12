from dataclasses import dataclass
import logging
from typing import Any, cast
from urllib.parse import ParseResult, parse_qs, urlparse

from yt_dlp import YoutubeDL
from hyperstreamkraken.sugar.coalesce import coalesce


@dataclass(frozen=True)
class YoutubeSearch:
    url: str
    id: str


def search_on_youtube(query: str) -> YoutubeSearch:
    search_query: str = f"ytsearch:{query}"

    yt_dlp_options: dict[str, Any] = {
        "format": "bestaudio/best",
        "noplaylist": True,
        "quiet": True,
        "logger": logging.getLogger(),
    }

    with YoutubeDL(yt_dlp_options) as ydl:  # pyright: ignore [reportArgumentType]
        info = ydl.extract_info(search_query, download=False)
        entries = coalesce(info.get("entries"), lambda: [])
        if not entries:
            raise RuntimeError(f"No YouTube results for '{query}'")

        video_info: dict[str, Any] = cast(dict[str, Any], entries[0])
        video_url: str = cast(str, video_info.get("webpage_url"))
        video_parsed_url: ParseResult = urlparse(video_url)
        video_url_params: dict[str, list[str]] = parse_qs(video_parsed_url.query)
        video_id_parameter: str = "v"

        if video_id_parameter not in video_url_params:
            raise ValueError(
                f"No '{video_id_parameter}' HTTP param in YouTube url: {video_url}"
            )

        video_id: str = video_url_params[video_id_parameter][0]

        return YoutubeSearch(url=video_url, id=video_id)
