import sub


def test_indices():
    assert abs(sub.efficiency(2, 2) - 2 ** 0.5) < 1e-12
    assert sub.efficiency(1.618, 1) > sub.efficiency(2, 2)


def test_counts():
    assert sub.evaluations_for_digits(2, 2, 1, 16) == 8
    assert sub.evaluations_for_digits(1.618, 1, 1, 16) == 6
    assert sub.bisect_evaluations(15) == 50
