import math
import numpy as np
import sub


def test_moments():
    rng = np.random.default_rng(0)
    x = sub.ou_exact_step(np.full(40000, 3.0), 0.7, 1.5, 1.0, 0.8, rng)
    m, v = sub.ou_mean_var(3.0, 0.7, 1.5, 1.0, 0.8)
    assert abs(x.mean() - m) < 0.01 and abs(x.var() / v - 1) < 0.03


def test_stationary():
    path = sub.ou_path(5.0, 60000, 0.1, 2.0, -1.0, 1.0, np.random.default_rng(1))[1000:]
    assert abs(path.mean() + 1) < 0.03 and abs(path.var() / sub.stationary_var(2.0, 1.0) - 1) < 0.06
    p = path - path.mean()
    for k in (1, 5):
        ac = np.dot(p[:-k], p[k:]) / np.dot(p, p)
        assert abs(ac - math.exp(-2.0 * 0.1 * k)) < 0.03
