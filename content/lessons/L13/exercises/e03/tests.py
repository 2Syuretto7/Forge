import numpy as np
import sub


def test_ulp():
    assert sub.ulp(1.0) == 2.0 ** -10 and sub.ulp(2048.0) == 2.0 and sub.ulp(1.5) == 2.0 ** -10
    assert sub.ulp(1.0, 8, 7) == 2.0 ** -7
    assert sub.ulp(1e-7) == 2.0 ** -24


def test_exact_integers():
    assert sub.largest_exact_integer(10) == 2048
    assert float(np.float16(2048) + np.float16(1)) == 2048.0
    assert float(np.float16(2047) + np.float16(1)) == 2048.0
    assert sub.largest_exact_integer(23) == 2 ** 24 and float(np.float32(2 ** 24) + np.float32(1)) == 2.0 ** 24
