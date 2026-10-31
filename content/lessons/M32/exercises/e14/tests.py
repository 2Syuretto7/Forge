import math
import numpy as np
import sub


def test_extremes_collapse():
    rng = np.random.default_rng(0)
    tiny = sub.ess_for_step(0.02, 10, 8000, rng)
    good = sub.ess_for_step(0.75, 10, 8000, rng)
    huge = sub.ess_for_step(20.0, 10, 8000, rng)
    assert tiny[0] > 0.95 and huge[0] < 0.02 and 0.15 < good[0] < 0.45
    assert good[1] > 8 * tiny[1] and good[1] > 8 * huge[1], (tiny, good, huge)


def test_best_step():
    st = sub.best_step([0.05, 0.15, 0.4, 0.75, 1.5, 4.0], 10, 5000, np.random.default_rng(1))
    assert 0.4 <= st <= 1.5


def test_separated_peaks():
    rng = np.random.default_rng(2)
    assert 0.3 < sub.mode_fraction(2.0, 1.0, 20000, rng) < 0.7
    assert sub.mode_fraction(12.0, 1.0, 20000, rng) < 0.01
