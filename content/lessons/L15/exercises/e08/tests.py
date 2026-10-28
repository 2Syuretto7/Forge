import numpy as np
import sub

rng = np.random.default_rng(11)


def runs(lo, hi, n=8):
    x = np.logspace(lo, hi, n)
    return x, 5.0 * x ** -0.1 * np.exp(0.01 * rng.standard_normal(n))


def test_interval_contains_the_truth():
    x, y = runs(15, 21)
    lo, hi = sub.bootstrap_exponent(x, y)
    assert lo < 0.1 < hi and hi - lo < 0.02


def test_narrow_range_is_less_certain():
    x, y = runs(15, 21)
    xn, yn = runs(15, 16)
    wide = np.subtract(*sub.bootstrap_exponent(x, y)[::-1])
    narrow = np.subtract(*sub.bootstrap_exponent(xn, yn)[::-1])
    assert narrow > 3 * wide


def test_reproducible():
    x, y = runs(15, 21)
    assert sub.bootstrap_exponent(x, y, seed=4) == sub.bootstrap_exponent(x, y, seed=4)
