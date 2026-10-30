import sub


def test_hundred_thousand():
    assert sub.dense_bytes(100_000) == 80 * 10 ** 9
    assert sub.sparse_bytes(10 ** 6) == 16 * 10 ** 6
    assert sub.iteration_flops(10 ** 6, 10 ** 5) == 2_300_000


def test_web():
    assert sub.sparse_bytes(10 ** 11, index_bytes=8) == 24 * 10 ** 11
    assert abs(sub.seconds(10 ** 10, 10 ** 11, 113, 1e12) - 113 * 2.3e11 / 1e12) < 1e-6
