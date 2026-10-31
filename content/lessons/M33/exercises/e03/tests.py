import numpy as np
import sub


def test_product():
    rng = np.random.default_rng(0)
    A, B = rng.standard_normal((96, 70)), rng.standard_normal((70, 50))
    for b in (32, 17, 200):
        assert np.allclose(sub.blocked_matmul(A, B, b), A @ B)


def test_traffic():
    n = 4096
    for b in (16, 52, 128):
        r = sub.traffic_naive(n) / sub.traffic_blocked(n, b)
        assert 0.9 * b < r <= b
    assert sub.best_tile(8192) == 52
    assert sub.best_tile(3 * 64 * 64) == 64
