from typing import Callable, cast


def coalesce[V: object](obj: V | None, or_else: V | Callable[[], V]) -> V:
    if obj is not None:
        return obj

    if isinstance(or_else, Callable):
        return cast(V, or_else())
    else:
        return or_else
