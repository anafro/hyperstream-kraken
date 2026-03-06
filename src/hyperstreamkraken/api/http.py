from functools import partial
import json
import logging
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any, override

from hyperstreamkraken.storage.song_storage import SongStorage


logger: logging.Logger = logging.getLogger(__name__)


def start_http_api_server(
    port: int,
    songs: SongStorage,
) -> None:
    class Handler(BaseHTTPRequestHandler):
        def __init__(self, request, client_address, server) -> None:
            super().__init__(request, client_address, server)

        def do_GET(self) -> Any:
            if self.path == "/up":
                self.send_response(200)
                self.end_headers()
                return self.wfile.write(b"Ok")

            return self.send_response(404)

        @override
        def log_message(self, format: str, *args: Any) -> None:
            logger.info(format, *args)

    HTTPServer(("0.0.0.0", port), Handler).serve_forever()


def start_http_api_server_daemon(port: int, songs: SongStorage) -> None:
    threading.Thread(
        target=partial(start_http_api_server, port=port, songs=songs), daemon=True
    ).start()
    logger.info("Service health route has started, use /up.")
