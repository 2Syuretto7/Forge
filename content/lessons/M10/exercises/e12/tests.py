import sub


def test_scores():
    assert sub.scores_bytes(8, 32, 4096) == 8 * 32 * 4096 * 4096 * 2
    assert sub.scores_bytes(1, 1, 1024, 4) == 4 * 2 ** 20


def test_intensity():
    assert sub.matmul_bytes(2, 3, 4) == (6 + 12 + 8) * 2
    assert abs(sub.intensity(4096, 4096, 4096) - 4096 / 3) < 1e-9
    assert sub.intensity(4096, 4096, 1) < 1.01
