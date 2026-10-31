import numpy as np
import sub


def test_intervals():
    correct = (np.random.default_rng(7).random(1000) < 0.92).astype(float)
    acc, lo, hi = sub.hoeffding_interval(correct)
    acc2, blo, bhi = sub.bootstrap_interval(correct)
    assert acc == acc2 and lo < 0.92 < hi and blo < 0.92 < bhi
    assert abs((hi - lo) / 2 - 0.04295) < 1e-4
    assert 2.0 < sub.width_ratio(correct) < 3.2


def test_balanced_case():
    correct = (np.random.default_rng(8).random(1000) < 0.5).astype(float)
    assert 1.1 < sub.width_ratio(correct) < 1.6
