import numpy as np
import sub

rng = np.random.default_rng(9)
X = rng.normal(size=(4, 3))
W = rng.normal(size=(3, 5))
G = rng.normal(size=(4, 5))


def _num(f, P, h=1e-6):
    g = np.zeros_like(P)
    for idx in np.ndindex(P.shape):
        E = np.zeros_like(P)
        E[idx] = h
        g[idx] = (f(P + E) - f(P - E)) / (2 * h)
    return g


def _rel(a, b):
    return np.linalg.norm(a - b) / (np.linalg.norm(a) + np.linalg.norm(b))


def test_shapes():
    dX, dW = sub.matmul_backward(X, W, G)
    assert dX.shape == X.shape and dW.shape == W.shape


def test_grad_X_matches_finite_differences():
    dX, _ = sub.matmul_backward(X, W, G)
    assert _rel(dX, _num(lambda P: sub.loss(P, W, G), X)) < 1e-5


def test_grad_W_matches_finite_differences():
    _, dW = sub.matmul_backward(X, W, G)
    assert _rel(dW, _num(lambda P: sub.loss(X, P, G), W)) < 1e-5
