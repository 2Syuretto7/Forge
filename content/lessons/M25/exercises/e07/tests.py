import math
import numpy as np
import sub

rng = np.random.default_rng(7)
X = rng.normal(size=(60, 3))
Y = X @ np.array([1.0, -2.0, 0.5]) + 0.3 * rng.normal(size=60)


def test_grad_w():
    w = np.array([0.2, -1.0, 1.5])
    g = sub.grad_w(w, 0.4, X, Y)
    h = 1e-6
    for k in range(3):
        e = np.zeros(3)
        e[k] = h
        num = (sub.nll(w + e, 0.4, X, Y) - sub.nll(w - e, 0.4, X, Y)) / (2 * h)
        assert abs(num - g[k]) < 1e-6


def test_fit_is_least_squares():
    w, s2 = sub.fit(X, Y)
    assert np.allclose(w, np.linalg.solve(X.T @ X, X.T @ Y))
    assert abs(s2 - np.mean((Y - X @ w) ** 2)) < 1e-12
    assert np.allclose(sub.grad_w(w, 0.0, X, Y), 0, atol=1e-10)


def test_perturbations_raise_the_loss():
    w, s2 = sub.fit(X, Y)
    s = 0.5 * math.log(s2)
    best = sub.nll(w, s, X, Y)
    for _ in range(10):
        assert sub.nll(w + 0.01 * rng.normal(size=3), s, X, Y) > best
    assert sub.nll(w, s + 0.05, X, Y) > best and sub.nll(w, s - 0.05, X, Y) > best
