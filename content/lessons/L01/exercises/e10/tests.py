import numpy as np
import sub

rng = np.random.default_rng(10)
Z = rng.normal(size=(200, 3))
X = Z * np.array([1.0, 1000.0, 30.0]) + np.array([0.0, 500.0, -20.0])
y = Z @ np.array([1.0, -2.0, 0.5]) + 0.1 * rng.normal(size=200)
y = y - y.mean()


def test_condition_numbers():
    assert sub.hessian_condition(X) > 1e5
    assert sub.hessian_condition(sub.standardize(X)) < 10


def test_standardization_makes_gd_fast():
    slow = sub.steps_to_converge(X, y, 1e-3, 20000)
    fast = sub.steps_to_converge(sub.standardize(X), y, 1e-3, 20000)
    assert fast < 100, fast
    assert slow == 20000 or slow > 100 * fast, (slow, fast)
