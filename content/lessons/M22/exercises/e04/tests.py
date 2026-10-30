import numpy as np
import sub


def test_fixed_points():
    for n in (2, 10, 52, 1000):
        assert abs(sub.expected_fixed_points(n) - 1) < 1e-12
    assert abs(sub.simulate_fixed_points(10, 20000, 4) - 1) < 0.04


def test_empty_bins_by_simulation():
    rng = np.random.default_rng(5)
    hits = rng.integers(0, 20, size=(20000, 30))
    empty = 20 - np.array([len(np.unique(r)) for r in hits])
    assert abs(empty.mean() - sub.expected_empty_bins(30, 20)) < 0.05


def test_birthdays():
    assert abs(sub.expected_distinct_birthdays(23) - 22.32) < 1e-3
    assert abs(sub.expected_distinct_birthdays(1) - 1) < 1e-12
