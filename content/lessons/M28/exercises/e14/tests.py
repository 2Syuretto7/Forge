import numpy as np
import sub


def test_minima():
    a, b = sub.minima()
    assert abs(sub.fprime(a)) < 1e-9 and abs(sub.fprime(b)) < 1e-9
    assert -1.1 < a < -1.0 and 0.9 < b < 1.0
    assert sub.f(a) < sub.f(b)
    h = 1e-4
    for x in (a, b):
        assert sub.f(x + h) - 2 * sub.f(x) + sub.f(x - h) > 0


def test_basins():
    starts = np.linspace(-2, 2, 201)
    frac = sub.basin_fraction(starts)
    assert 0.5 < frac < 0.56, frac
    assert sub.descend(1.5) > 0 and sub.descend(-1.5) < 0
