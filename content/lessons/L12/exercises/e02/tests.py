import numpy as np
import sub

rng = np.random.default_rng(2)


def test_matches_product():
    A, B = rng.normal(size=(10, 7)), rng.normal(size=(7, 9))
    C, _ = sub.tiled_matmul(A, B, 4)
    assert np.allclose(C, A @ B)


def test_loads():
    n, T = 16, 4
    A, B = rng.normal(size=(n, n)), rng.normal(size=(n, n))
    _, loads = sub.tiled_matmul(A, B, T)
    assert loads == 2 * n ** 3 // T
    _, loads1 = sub.tiled_matmul(A, B, 1)
    assert loads1 == 2 * n ** 3
