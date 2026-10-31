import math
import struct
import numpy as np
import sub


def test_known_patterns():
    assert sub.float32_bits(1.0) == 0x3F800000
    assert sub.decode(0x3F800000) == (0, 127, 0, 1.0)
    assert sub.decode(0xC0000000)[3] == -2.0
    assert sub.decode(0x7F800000)[3] == math.inf and math.isnan(sub.decode(0x7FC00000)[3])
    assert sub.decode(1)[3] == 2.0**-149


def test_round_trip():
    rng = np.random.default_rng(1)
    for b in rng.integers(0, 2**32, size=2000):
        b = int(b)
        if (b >> 23) & 0xFF == 255:
            continue
        assert sub.decode(b)[3] == struct.unpack(">f", struct.pack(">I", b))[0]
    assert sub.decode(sub.float32_bits(0.1))[3] == 0.10000000149011612


def test_spacing():
    assert sub.spacing(1.0) == 2.0**-23
    assert sub.spacing(2.0**24) == 2.0
    assert sub.spacing(1000.0) == 2.0**-14
