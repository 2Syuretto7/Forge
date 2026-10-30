import sub


def test_order_of_magnitude():
    assert sub.order_of_magnitude(4096) == 3
    assert sub.order_of_magnitude(0.05) == -2
    assert sub.order_of_magnitude(1e15) == 15
    assert sub.order_of_magnitude(-2.5e9) == 9
    assert sub.order_of_magnitude(999.9999) == 2


def test_nearest_power_switches_at_root_ten():
    assert sub.nearest_power(3.1) == 0
    assert sub.nearest_power(3.2) == 1
    assert sub.nearest_power(2e12) == 12
    assert sub.nearest_power(5e12) == 13


def test_within_factor():
    assert sub.within_factor(300, 100, 3)
    assert sub.within_factor(100, 300, 3)
    assert not sub.within_factor(100, 301, 3)


def test_ladder():
    vals = [1.24e8, 8.64e4, 8e9, 1]
    assert sub.ladder(vals) == [(0, 1), (4, 8.64e4), (8, 1.24e8), (9, 8e9)]
