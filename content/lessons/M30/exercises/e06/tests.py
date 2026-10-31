import numpy as np
import sub

rng = np.random.default_rng(6)
X = rng.normal(size=(200, 3))
Y = np.sign(X @ np.array([1.0, -2.0, 0.5]) + 0.5 * rng.normal(size=200))


def primal(w, C):
    return 0.5 * w @ w + C * np.sum(np.maximum(0, 1 - Y * (X @ w)))


def test_grad_dual():
    a = rng.uniform(0, 0.5, size=200)
    g = sub.dual_grad(a, X, Y)
    h = 1e-6
    for i in (0, 17, 199):
        e = np.zeros(200)
        e[i] = h
        num = (sub.dual_objective(a + e, X, Y) - sub.dual_objective(a - e, X, Y)) / (2 * h)
        assert abs(num - g[i]) < 1e-5


def test_gap_closes():
    a, w = sub.coordinate_ascent(X, Y, 1.0, 400, np.random.default_rng(1))
    assert a.min() >= 0 and a.max() <= 1.0
    assert np.allclose(w, X.T @ (a * Y))
    gap = primal(w, 1.0) - sub.dual_objective(a, X, Y)
    assert 0 <= gap < 1e-6 * primal(w, 1.0), gap
