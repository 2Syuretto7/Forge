import sub


def test_arithmetic_and_geometric():
    assert sub.arithmetic(3, 4, 5) == [3, 7, 11, 15, 19]
    assert sub.geometric(1, 2, 6) == [1, 2, 4, 8, 16, 32]
    assert sub.geometric(5, 0.5, 3) == [5, 2.5, 1.25]


def test_recurrence():
    assert sub.recurrence(lambda x: 2 * x + 1, 0, 5) == [0, 1, 3, 7, 15]
    xs = sub.recurrence(lambda x: (x + 2 / x) / 2, 1.0, 6)
    assert abs(xs[-1] - 2 ** 0.5) < 1e-12, "Newton's recurrence for sqrt(2) settles fast"
    assert sub.recurrence(abs, -3, 1) == [-3]


def test_nth():
    assert sub.nth_arithmetic(3, 4, 4) == 19
    assert sub.nth_arithmetic(10, -2, 100) == -190
