import numpy as np
import sub


def unit(n, d, seed):
    X = np.random.default_rng(seed).normal(size=(n, d))
    return X / np.linalg.norm(X, axis=1, keepdims=True)


def test_estimate_below_bound():
    X = unit(200, 5, 1)
    est = sub.rademacher_linear(X, 2.0, 4000, np.random.default_rng(2))
    bound = sub.rademacher_bound(X, 2.0)
    assert 0.85 * bound < est <= bound + 1e-12
    assert abs(bound - 2.0 / np.sqrt(200)) < 1e-12


def test_one_over_sqrt_n():
    a = sub.rademacher_linear(unit(100, 5, 3), 1.0, 3000, np.random.default_rng(4))
    b = sub.rademacher_linear(unit(1600, 5, 5), 1.0, 3000, np.random.default_rng(6))
    assert abs(a / b - 4) < 0.4
