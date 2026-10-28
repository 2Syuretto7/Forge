import numpy as np
import sub

rng = np.random.default_rng(4)
X = rng.normal(size=(4, 5)) * 2 + 0.5
G = rng.normal(size=5) + 1
DY = rng.normal(size=(4, 5))


def _num(f, P, h=1e-6):
    g = np.zeros_like(P)
    for idx in np.ndindex(P.shape):
        E = np.zeros_like(P)
        E[idx] = h
        g[idx] = (f(P + E) - f(P - E)) / (2 * h)
    return g


def test_forward():
    y, _ = sub.rmsnorm_forward(np.array([[3.0, 4.0]]), np.ones(2), eps=0.0)
    assert np.allclose(y, [[3 / np.sqrt(12.5), 4 / np.sqrt(12.5)]])
    y, _ = sub.rmsnorm_forward(X, np.ones(5))
    assert np.allclose(np.sqrt((y ** 2).mean(axis=1)), 1, atol=1e-6)


def test_grad_both():
    f = lambda x, g: float(np.sum(sub.rmsnorm_forward(x, g)[0] * DY))
    _, cache = sub.rmsnorm_forward(X, G)
    dx, dg = sub.rmsnorm_backward(DY, cache)
    assert np.allclose(dx, _num(lambda P: f(P, G), X), atol=1e-6)
    assert np.allclose(dg, _num(lambda P: f(X, P), G), atol=1e-6)


def test_not_centered():
    y, _ = sub.rmsnorm_forward(np.ones((1, 4)) * 5, np.ones(4))
    assert np.allclose(y, 1, atol=1e-6)
