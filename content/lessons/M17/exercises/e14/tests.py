import sub


def test_aliasing():
    assert sub.points_per_period(32) < 2
    assert sub.simpson_error(32) > 1e-3


def test_enough_points():
    n = sub.first_good_n()
    assert 1024 <= n <= 8192, n
    assert sub.points_per_period(n) > 30
