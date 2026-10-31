import sub


def test_gd_linear():
    ks = [10, 100, 1000]
    s = sub.loglog_slope(ks, [sub.count("gd", k) for k in ks])
    assert 0.9 < s < 1.05, s


def test_momentum_square_root():
    ks = [10, 100, 1000, 10000]
    c = [sub.count("heavy", k) for k in ks]
    s = sub.loglog_slope(ks, c)
    assert 0.4 < s < 0.6, (s, c)
