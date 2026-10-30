import sub


def test_gap():
    assert sub.gap(3, 2) == 1 and sub.gap(7, 5) == 1 and sub.gap(4, 3) == 2


def test_never_zero():
    assert sub.smallest_gap(20000) == 1


def test_closest_fractions():
    assert sub.closest_fractions(100) == [(1, 1), (3, 2), (7, 5), (17, 12), (41, 29), (99, 70)]
    p, q = sub.best_fraction(12)
    assert (p, q) == (17, 12)
