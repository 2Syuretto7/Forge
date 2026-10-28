import numpy as np
import sub

rng = np.random.default_rng(3)
X = rng.normal(size=(5, 6)) * 2 - 1
G = rng.normal(size=6) + 1
B = rng.normal(size=6)
DY = rng.normal(size=(5, 6))


def _num(f, P, h=1e-6):
    g = np.zeros_like(P)
    for idx in np.ndindex(P.shape):
        E = np.zeros_like(P)
        E[idx] = h
        g[idx] = (f(P + E) - f(P - E)) / (2 * h)
    return g


def test_forward():
    y, _ = sub.layernorm_forward(X, np.ones(6), np.zeros(6))
    assert np.allclose(y.mean(axis=1), 0, atol=1e-12) and np.allclose(y.var(axis=1), 1, atol=1e-5)


def test_grad_all_three():
    f = lambda x, g, b: float(np.sum(sub.layernorm_forward(x, g, b)[0] * DY))
    _, cache = sub.layernorm_forward(X, G, B)
    dx, dg, db = sub.layernorm_backward(DY, cache)
    assert np.allclose(dx, _num(lambda P: f(P, G, B), X), atol=1e-6)
    assert np.allclose(dg, _num(lambda P: f(X, P, B), G), atol=1e-6)
    assert np.allclose(db, _num(lambda P: f(X, G, P), B), atol=1e-6)


def test_rows_are_independent():
    y_all, _ = sub.layernorm_forward(X, G, B)
    y_one, _ = sub.layernorm_forward(X[2:3], G, B)
    assert np.allclose(y_all[2], y_one[0])
