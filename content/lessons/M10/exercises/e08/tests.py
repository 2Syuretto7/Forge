import numpy as np
import sub

rng = np.random.default_rng(0)


def test_blocks():
    for m, n, p, bs in [(7, 5, 6, 2), (16, 16, 16, 4), (10, 3, 9, 4), (5, 5, 5, 8)]:
        A, B = rng.normal(size=(m, n)), rng.normal(size=(n, p))
        assert np.allclose(sub.block_matmul(A, B, bs), A @ B)


def test_count():
    assert sub.tile_count(7, 5, 6, 2) == 4 * 3 * 3
    assert sub.tile_count(4096, 4096, 4096, 128) == 32 ** 3
