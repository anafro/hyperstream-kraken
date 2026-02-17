from functools import partial
import logging
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any, override


logger: logging.Logger = logging.getLogger(__name__)


def start_listening_http_up_route_blocking(port: int) -> None:
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:
            if self.path == "/up":
                self.send_response(200)
                self.end_headers()
                _ = self.wfile.write(b"OK")

        @override
        def log_message(self, format: str, *args: Any) -> None:
            pass

    HTTPServer(("0.0.0.0", port), Handler).serve_forever()


def start_listening_http_up_route_daemon(port: int) -> None:
    threading.Thread(
        target=partial(start_listening_http_up_route_blocking, port=port), daemon=True
    ).start()
    logger.info("Service health route has started, use /up.")
