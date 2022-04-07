"""
FastLZ1 Decompression
"""

import io
import struct
from typing import BinaryIO


def fastlz1_decompress(
    ibuf: BinaryIO,
    obuf: BinaryIO
) -> None:
    """
    Port of fastlz1_decompress reference implementation
    """

    opcode_0 = ibuf.read(1)
    opcode_0 = struct.pack('B', opcode_0[0] & 31)

    while len(opcode_0) == 1:
        opcode = opcode_0[0]

        op_type = opcode >> 5
        op_data = opcode & 31

        if op_type == 0b000:
            # literal run
            run = 1 + op_data

            literal = ibuf.read(run)
            obuf.write(literal)

        elif op_type == 0b111:
            # long match
            opcode_1, opcode_2 = ibuf.read(2)

            ofs = (op_data << 8) + opcode_2

            match_len = 9 + opcode_1

            _pos = obuf.tell()
            obuf.seek(-ofs, io.SEEK_CUR)
            copy = obuf.read(match_len)
            obuf.seek(_pos, io.SEEK_SET)
            obuf.write(copy)

        else:
            # short match
            opcode_1 = ibuf.read(1)[0]

            match_len = 2 + op_type
            ofs = (op_data << 8) + opcode_1

            _pos = obuf.tell()
            obuf.seek(-ofs, io.SEEK_CUR)
            copy = obuf.read(match_len)
            obuf.seek(_pos, io.SEEK_SET)
            obuf.write(copy)

        opcode_0 = ibuf.read(1)
