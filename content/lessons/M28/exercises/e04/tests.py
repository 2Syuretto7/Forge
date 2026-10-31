import numpy as np
import sub

rng = np.random.default_rng(4)
X = rng.normal(size=(200, 3))
Y = (X @ np.array([1.5, -2.0, 0.5]) + rng.normal(size=200) > 0).astype(float)


def test_grad_logistic():
    w = np.array([0.3, -0.2, 1.0])
    g = sub.logistic_grad(w, X, Y)
    h = 1e-6
    for k in range(3):
        e = np.zeros(3)
        e[k] = h
        num = (sub.logistic_loss(w + e, X, Y) - sub.logistic_loss(w - e, X, Y)) / (2 * h)
        assert abs(num - g[k]) < 1e-7


def test_tangent_planes_lie_below():
    f = lambda w: sub.logistic_loss(w, X, Y)
    g = lambda w: sub.logistic_grad(w, X, Y)
    for _ in range(50):
        a, b = rng.normal(size=3) * 3, rng.normal(size=3) * 3
        assert sub.tangent_gap(f, g, a, b) >= -1e-12


def test_nonconvex_has_a_negative_gap():
    f = lambda v: float(np.sin(v[0]))
    g = lambda v: np.array([np.cos(v[0])])
    gaps = [sub.tangent_gap(f, g, [a], [b]) for a, b in rng.uniform(-3, 3, size=(50, 2))]
    assert min(gaps) < -0.1
