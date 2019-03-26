from typing import List, Generator


def mm_encode(source: Generator[bytes, None, None]) -> Generator[bytes, None, None]:
    for byte in source:
        # TODO: Do something sensible.
        yield byte


def mm_decode(source: Generator[bytes, None, None]) -> Generator[bytes, None, None]:
    for byte in source:
        # TODO: Do something sensible.
        yield byte
