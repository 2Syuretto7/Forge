import math
import struct
import numpy as np


def float32_bits(x):
    """The 32-bit pattern of x rounded to float32."""
    return struct.unpack(">I", struct.pack(">f", x))[0]


def decode(bits):
    """(sign, exponent, fraction, value) of a float32 bit pattern."""
    s = bits >> 31
    e = (bits >> 23) & 0xFF
    f = bits & 0x7FFFFF
    if e == 255:
        v = math.nan if f else math.inf
    elif e == 0:
        v = f * 2.0**-149
    else:
        v = (1 + f / 2**23) * 2.0 ** (e - 127)
    return s, e, f, -v if s else v


def spacing(x):
    """Gap to the next larger float32."""
    return float(np.spacing(np.float32(x)))
