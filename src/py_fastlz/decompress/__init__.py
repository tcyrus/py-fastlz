"""
FastLZ Decompression
"""

import io
from typing import Optional

from ..utils import BufferedRandom

from .fastlz1 import fastlz1_decompress
from .fastlz2 import fastlz2_decompress


def decompress(
    data: bytes,
    level: Optional[int] = None,
    bufsize: Optional[int] = None
) -> bytes:
    """
    decompression function designed to mimic zlib.decompress
    """

    # if compression level isn't provided
    # we use the magic identifier
    if level is None:
        level = (data[0] >> 5) + 1

    with BufferedRandom(io.BytesIO(), bufsize) as obuf:
        with io.BytesIO(data) as ibuf:
            if level == 1:
                fastlz1_decompress(ibuf, obuf)
            elif level == 2:
                fastlz2_decompress(ibuf, obuf)

        # obuf.truncate()
        obuf.seek(0, whence=io.SEEK_SET)
        return obuf.read()
