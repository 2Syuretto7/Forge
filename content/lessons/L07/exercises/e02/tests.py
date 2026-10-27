import numpy as np
import sub

rng = np.random.default_rng(2)
Z = rng.normal(size=(6, 5))
Z[np.abs(Z) < 1e-3] = 0.5
G = rng.normal(size=(6, 5))


def _num(f, P, h=1e-6):
    g = np.zeros_like(P)
    for idx in np.ndindex(P.shape):
        E = np.zeros_like(P)
        E[idx] = h
        g[idx] = (f(P + E) - f(P - E)) / (2 * h)
    return g


def _rel(a, b):
    return np.linalg.norm(a - b) / (np.linalg.norm(a) + np.linalg.norm(b))


def test_grad_relu():
    Y, c = sub.relu_forward(Z)
    assert np.allclose(Y, np.maximum(Z, 0))
    dZ = sub.relu_backward(G, c)
    assert _rel(dZ, _num(lambda P: np.sum(sub.relu_forward(P)[0] * G), Z)) < 1e-5


def test_grad_tanh():
    _, c = sub.tanh_forward(Z)
    dZ = sub.tanh_backward(G, c)
    assert _rel(dZ, _num(lambda P: np.sum(sub.tanh_forward(P)[0] * G), Z)) < 1e-5


def test_relu_derivative_at_zero_is_zero():
    _, c = sub.relu_forward(np.zeros((1, 3)))
    assert np.all(sub.relu_backward(np.ones((1, 3)), c) == 0)
