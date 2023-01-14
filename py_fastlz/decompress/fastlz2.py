"""
FastLZ2 Decompression
"""

import io
import struct

from ..consts import MAX_L2_DISTANCE


def fastlz2_decompress(
    ibuf: io.BytesIO,
    obuf: io.BufferedRandom
) -> None:

    opcode_0 = ibuf.read(1)
    opcode_0[0] &= 31

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
            match_len = 9

            while True:
                nn = ibuf.read(1)[0]
                match_len += nn
                if nn != 255:
                    break

            ofs = op_data << 8
            ofs += ibuf.read(1)[0]

            if ofs == MAX_L2_DISTANCE:
                # match from 16-bit distance
                ofs += struct.unpack('=h', ibuf.read(2))[0]

            obuf.seek(-ofs, whence=io.SEEK_CUR)
            copy = obuf.read(match_len)
            obuf.seek(0, whence=io.SEEK_END)
            obuf.write(copy)

        else:
            # short match
            match_len = 2 + op_type

            ofs = op_data << 8
            ofs += ibuf.read(1)[0]

            if ofs == MAX_L2_DISTANCE:
                # match from 16-bit distance
                _ofs = ibuf.read(2)
                ofs += _ofs[0] << 8
                ofs += _ofs[1]

            obuf.seek(-ofs, whence=io.SEEK_CUR)
            copy = obuf.read(match_len)
            obuf.seek(0, whence=io.SEEK_END)
            obuf.write(copy)

        opcode_0 = ibuf.read(1)
