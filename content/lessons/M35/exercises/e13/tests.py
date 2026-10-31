import numpy as np
import sub


def test_floor_matters():
    rng = np.random.default_rng(0)
    x = np.logspace(0, 2, 30)
    y = 1.7 + 2.0 * x**-0.5 + 0.003 * rng.standard_normal(30)
    truth = 1.7 + 2.0 * 1e5**-0.5
    ll, fl = sub.extrapolation_errors(x, y, 1e5, truth)
    assert ll < -0.1 and abs(fl) < 0.01, (ll, fl)
    A, alpha = sub.fit_loglog(x, y)
    assert A * 1e5 ** (-alpha) < 1.7
