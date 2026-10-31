import numpy as np
import sub

rng = np.random.default_rng(1)
X = rng.normal(size=(5, 4))
W = rng.normal(size=(4, 3))
b = rng.normal(size=3)
G = rng.normal(size=(5, 3))


def _loss(X, W, b):
    return float(np.sum(sub.linear_forward(X, W, b)[0] * G))


def _num(f, P, h=1e-6):
    g = np.zeros_like(P)
    for idx in np.ndindex(P.shape):
        E = np.zeros_like(P)
        E[idx] = h
        g[idx] = (f(P + E) - f(P - E)) / (2 * h)
    return g


def _rel(a, b):
    return np.linalg.norm(a - b) / (np.linalg.norm(a) + np.linalg.norm(b))


def test_forward():
    Y, _ = sub.linear_forward(X, W, b)
    assert np.allclose(Y, X @ W + b)


def test_grad_all_three():
    _, cache = sub.linear_forward(X, W, b)
    dX, dW, db = sub.linear_backward(G, cache)
    assert dX.shape == X.shape and dW.shape == W.shape and db.shape == b.shape
    assert _rel(dX, _num(lambda P: _loss(P, W, b), X)) < 1e-5
    assert _rel(dW, _num(lambda P: _loss(X, P, b), W)) < 1e-5
    assert _rel(db, _num(lambda P: _loss(X, W, P), b)) < 1e-5
