import sub


def test_counts():
    assert sub.standard_io(4, 2) == 4 * 4 * 2 + 4 * 16
    assert abs(sub.flash_io(4096, 64, 25000) - (4096 ** 2 * 64 ** 2 / 25000 + 4 * 4096 * 64)) < 1e-6


def test_ratio_grows_with_length():
    r1, r4 = sub.io_ratio(1024, 64, 25000), sub.io_ratio(4096, 64, 25000)
    assert 10 < r1 < r4 < 4 * 25000 / 64 ** 2 + 1
