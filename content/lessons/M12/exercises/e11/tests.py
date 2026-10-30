import sub


def test_values():
    assert sub.flops_normal(100, 10) == 100 * 100 + 2000 + 1000 / 3
    assert abs(sub.flops_qr(100, 10) - (20000 - 2000 / 3 + 4000 + 100)) < 1e-9


def test_ratio():
    assert abs(sub.ratio(10 ** 7, 50) - 2) < 0.01
    assert 0.9 < sub.ratio(500, 500) < 1.1
