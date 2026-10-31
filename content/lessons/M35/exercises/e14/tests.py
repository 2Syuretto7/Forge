import numpy as np
import sub


def test_band_misses_a_break():
    rng = np.random.default_rng(0)
    x = np.logspace(0, 2, 30)
    y = sub.broken_law(x) + 0.003 * rng.standard_normal(30)
    p, h = sub.fit_and_band(x, y, 500.0)
    assert sub.inside(p, h, float(sub.broken_law(500.0)))
    p, h = sub.fit_and_band(x, y, 1e5)
    assert not sub.inside(p, h, float(sub.broken_law(1e5)))
    assert abs(sub.broken_law(1e3 + 1e-9) - sub.broken_law(1e3)) < 1e-9
