import numpy as np
import sub


def test_binomial():
    x = sub.binomial_by_sum(20, 0.3, 100000, np.random.default_rng(8))
    assert x.shape == (100000,) and x.min() >= 0 and x.max() <= 20
    m, v = sub.moments(x)
    assert abs(m - 6) < 0.03 and abs(v - 4.2) < 0.08


def test_poisson():
    for lam in (0.5, 4.0, 12.0):
        x = sub.poisson_by_arrivals(lam, 100000, np.random.default_rng(9))
        m, v = sub.moments(x)
        assert abs(m - lam) < 5 * np.sqrt(lam / 100000) and abs(v / lam - 1) < 0.03, (lam, m, v)
    x = sub.poisson_by_arrivals(2.0, 200000, np.random.default_rng(10))
    assert abs(np.mean(x == 0) - np.exp(-2)) < 0.003


def test_moments():
    assert sub.moments([1, 2, 3, 4]) == (2.5, 5 / 3)
