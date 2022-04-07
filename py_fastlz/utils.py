"""
Python Utils / Helpers for FastLZ
"""

import io
from typing import Optional


class SizedBytesIO(io.BytesIO):
    """
    Helper class since the io.BytesIO constructor doesn't have
    a way to specify the buffer size and the bytearray constructor
    doesn't handle NoneType as an arg
    """
    def __init__(
        self,
        buffer_size: Optional[int] = None
    ):
        if buffer_size is None:
            super().__init__()
        else:
            super().__init__(bytearray(buffer_size))
