import numpy as np
import sub

rng = np.random.default_rng(12)
Z = rng.normal(size=(200, 3))
X = np.column_stack([np.ones(200), Z])
y = (Z @ np.array([1.5, -1.0, 0.5]) + rng.logistic(size=200) > 0).astype(float)


def test_converges_fast():
    w, norms = sub.newton(X, y, 1e-3, 10)
    assert len(norms) == 10
    assert min(norms) < 1e-10, norms


def test_quadratic_convergence():
    _, norms = sub.newton(X, y, 1e-3, 10)
    tail = [g for g in norms if 1e-12 < g < 1e-2]
    assert len(tail) >= 2
    for a, b in zip(tail, tail[1:]):
        assert b < 50 * a * a + 1e-14, (a, b)


def test_matches_gradient_descent():
    w, _ = sub.newton(X, y, 1e-3, 10)
    v = np.zeros(4)
    for _ in range(20000):
        s = 0.5 * (1 + np.tanh(0.5 * (X @ v)))
        v -= 1.0 * (X.T @ (s - y) / 200 + 1e-3 * v)
    assert np.allclose(w, v, atol=1e-5)
