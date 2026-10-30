import numpy as np
import sub


def test_squared():
    a, g = sub.conds(6)
    assert 0.5 < np.log10(g) / (2 * np.log10(a)) < 1.1


def test_digits():
    a, g = sub.conds(15)
    assert sub.digits_kept(a) > 3
    assert sub.digits_kept(g) == 0
    assert sub.digits_kept(1.0) == 16


def test_chebyshev_rescues():
    assert sub.better_basis(15) < 10
    assert sub.conds(15)[0] > 1e10
