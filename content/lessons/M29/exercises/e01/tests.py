import numpy as np
import sub

rng = np.random.default_rng(1)
X = rng.normal(size=(300, 4))
Y = (X @ np.array([1.0, -1.0, 0.5, 0.0]) + rng.normal(size=300) > 0).astype(float)


def test_grad_logistic():
    w = np.array([0.2, -0.3, 0.1, 0.4])
    g = sub.grad(w, X, Y)
    h = 1e-6
    for k in range(4):
        e = np.zeros(4)
        e[k] = h
        assert abs((sub.loss(w + e, X, Y) - sub.loss(w - e, X, Y)) / (2 * h) - g[k]) < 1e-7


def test_descent_lemma():
    assert sub.descent_lemma_holds(X, Y, np.zeros(4), 200)


def test_sublinear_bound():
    L = np.linalg.eigvalsh(X.T @ X)[-1] / (4 * 300)
    long = sub.gd(X, Y, np.zeros(4), 1 / L, 20000)
    w_star, f_star = long[-1], sub.loss(long[-1], X, Y)
    r2 = float(w_star @ w_star)
    for k in (10, 100, 1000):
        assert sub.loss(long[k], X, Y) - f_star <= L * r2 / (2 * k) + 1e-9
