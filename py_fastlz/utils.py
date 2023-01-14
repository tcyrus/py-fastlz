"""
Python Utils / Helpers for FastLZ
"""

import io
from typing import Optional


class BufferedRandom(io.BufferedRandom):
    """
    Helper subclass for io.BufferedRandom since
    constructor doesn't use default on NoneType buffer_size
    """
    def __init__(
        self,
        raw: io.RawIOBase,
        buffer_size: Optional[int] = None
    ):
        if buffer_size is None:
            buffer_size = io.DEFAULT_BUFFER_SIZE

        # kwargs = {'buffer_size': buffer_size}
        # kwargs = {k:v for k, v in kwargs.items() if v is not None}
        # super().__init__(raw, **kwargs)

        super().__init__(raw, buffer_size=buffer_size)
