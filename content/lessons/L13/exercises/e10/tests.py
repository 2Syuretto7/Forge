import sub


def test_bytes():
    assert sub.score_bytes(8, 12, 2048) == 805_306_368
    assert sub.score_bytes(1, 1, 10, bytes_per=4) == 400


def test_intensity():
    assert abs(sub.scores_intensity(2048, 64) - 2 * 2048 * 2048 * 64 / (2 * (2 * 2048 * 64 + 2048 ** 2))) < 1e-9
    assert 63 < sub.scores_intensity(10 ** 6, 64) < 64


def test_max_ctx():
    n = sub.max_ctx_for_memory(16e9, 8, 12)
    assert sub.score_bytes(8, 12, n) <= 16e9 < sub.score_bytes(8, 12, n + 1)
