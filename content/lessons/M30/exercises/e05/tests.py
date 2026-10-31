import numpy as np
import sub

rng = np.random.default_rng(5)
X = rng.normal(size=(300, 3))
Y = np.sign(X @ np.array([2.0, -1.0, 0.5]) + 0.3 * rng.normal(size=300))


def test_subgradient_method():
    w = sub.subgradient_descent(X, Y, 0.1, 500)
    assert sub.primal_objective(w, X, Y, 0.1) < 0.5 * sub.primal_objective(np.zeros(3), X, Y, 0.1)
    assert np.mean(np.sign(X @ w) == Y) > 0.9


def test_points_outside_the_margin_do_not_count():
    w = np.array([3.0, -1.5, 0.7])
    v = sub.margin_violations(w, X, Y)
    g = sub.subgradient(w, X, Y, 0.1)
    assert np.allclose(g, w - 0.1 * (Y[v] @ X[v]))
    far = ~v
    assert np.allclose(sub.subgradient(w, X[far], Y[far], 0.1), w)
