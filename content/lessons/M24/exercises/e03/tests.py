import numpy as np
import sub


def test_square():
    est, se = sub.mc_integrate(lambda x: x * x, 0.0, 1.0, 100000, np.random.default_rng(3))
    assert abs(est - 1 / 3) < 4 * se and 0 < se < 0.002


def test_pi():
    est, se = sub.mc_integrate(lambda x: 4 * np.sqrt(1 - x * x), 0.0, 1.0, 200000, np.random.default_rng(4))
    assert abs(est - np.pi) < 4 * se


def test_error_bar_halves():
    _, s1 = sub.mc_integrate(np.exp, -1.0, 2.0, 10000, np.random.default_rng(5))
    _, s4 = sub.mc_integrate(np.exp, -1.0, 2.0, 40000, np.random.default_rng(6))
    assert abs(s4 / s1 - 0.5) < 0.05
