from typing import Never


def todo(message: str) -> Never:
    raise NotImplementedError(f"TODO: {message}")
