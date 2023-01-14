"""
FastLZ1 Decompression
"""

import io


def fastlz1_decompress(
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
            opcode_1, opcode_2 = ibuf.read(2)

            ofs = (op_data << 8) + opcode_2

            match_len = 9 + opcode_1

            obuf.seek(-ofs, whence=io.SEEK_CUR)
            copy = obuf.read(match_len)
            obuf.seek(0, whence=io.SEEK_END)
            obuf.write(copy)

        else:
            # short match
            opcode_1 = ibuf.read(1)[0]

            match_len = 2 + op_type
            ofs = (op_data << 8) + opcode_1

            obuf.seek(-ofs, whence=io.SEEK_CUR)
            copy = obuf.read(match_len)
            obuf.seek(0, whence=io.SEEK_END)
            obuf.write(copy)

        opcode_0 = ibuf.read(1)
