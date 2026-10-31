import numpy as np
import sub


def test_bivariate():
    for rho in (0.5, 0.9):
        s = sub.gibbs_bivariate(rho, 40000, np.random.default_rng(2))
        assert abs(np.corrcoef(s.T)[0, 1] - rho) < 0.03
        assert abs(sub.lag1(s[:, 0]) - rho**2) < 0.03
    slow = sub.gibbs_bivariate(0.99, 40000, np.random.default_rng(3))
    assert sub.lag1(slow[:, 0]) > 0.97


def test_general_gaussian():
    C = np.array([[2.0, 0.6, 0.3], [0.6, 1.0, -0.4], [0.3, -0.4, 1.5]])
    s = sub.gibbs_gaussian([1.0, -1.0, 0.5], C, 20000, np.random.default_rng(4))
    assert np.max(np.abs(s.mean(axis=0) - [1.0, -1.0, 0.5])) < 0.08
    assert np.max(np.abs(np.cov(s.T) - C)) < 0.1
