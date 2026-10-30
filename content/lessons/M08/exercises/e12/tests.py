import math
import sub


def test_billion_documents():
    b = sub.bits_needed(10 ** 9, 1e-6)
    assert b == 79
    assert math.comb(10 ** 9, 2) / 2 ** b <= 1e-6 < math.comb(10 ** 9, 2) / 2 ** (b - 1)


def test_capacity():
    n = sub.max_documents(64, 1e-6)
    assert math.comb(n, 2) / 2 ** 64 <= 1e-6 < math.comb(n + 1, 2) / 2 ** 64
    assert 6e6 < n < 6.2e6
