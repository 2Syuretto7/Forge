import numpy as np
import sub


def test_duplicates_break_the_interval():
    accs = sub.duplicated_accuracies(0.8, 100, 10, 20000, np.random.default_rng(2))
    naive = sub.naive_coverage(accs, 0.8, 1000)
    honest = sub.naive_coverage(accs, 0.8, sub.effective_n(1000, 10))
    assert 0.68 < naive < 0.78, naive
    assert honest > 0.99, honest
