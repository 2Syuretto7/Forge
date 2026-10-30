import sub


def test_bytes():
    assert sub.activation_bytes(96, 12288, 2048) == 4 * 96 * 12288 * 2048
    assert sub.best_k(100) == 10
    assert sub.checkpoint_bytes(100, 1000, 10, 10) == 4 * 20 * 1000 * 10
    assert sub.checkpoint_bytes(100, 1000, 10, 10) < sub.activation_bytes(100, 1000, 10) / 4
    assert sub.extra_compute(1) == 0.0 and sub.extra_compute(10) == 1.0
