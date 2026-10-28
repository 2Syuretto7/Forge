import numpy as np
import sub

rng = np.random.default_rng(1)
X = rng.normal(size=(6, 4)) * 3 + 1
G = rng.normal(size=4) + 1
B = rng.normal(size=4)
DY = rng.normal(size=(6, 4))


def _num(f, P, h=1e-6):
    g = np.zeros_like(P)
    for idx in np.ndindex(P.shape):
        E = np.zeros_like(P)
        E[idx] = h
        g[idx] = (f(P + E) - f(P - E)) / (2 * h)
    return g


def test_forward_statistics():
    y, _ = sub.batchnorm_forward(X, np.ones(4), np.zeros(4))
    assert np.allclose(y.mean(axis=0), 0, atol=1e-12)
    assert np.allclose(y.var(axis=0), 1, atol=1e-5)
    y2, _ = sub.batchnorm_forward(X, G, B)
    assert np.allclose(y2, G * y + B)


def test_grad_all_three():
    f = lambda x, g, b: float(np.sum(sub.batchnorm_forward(x, g, b)[0] * DY))
    _, cache = sub.batchnorm_forward(X, G, B)
    dx, dg, db = sub.batchnorm_backward(DY, cache)
    assert np.allclose(dx, _num(lambda P: f(P, G, B), X), atol=1e-6)
    assert np.allclose(dg, _num(lambda P: f(X, P, B), G), atol=1e-6)
    assert np.allclose(db, _num(lambda P: f(X, G, P), B), atol=1e-6)


def test_shift_and_scale_invariance():
    # With a negligible eps the normalized values have exactly unit variance, and gradients that
    # only shift or rescale the batch are removed entirely.
    _, cache = sub.batchnorm_forward(X, G, B, eps=1e-12)
    xh = cache[0]
    dx1, _, _ = sub.batchnorm_backward(np.ones((6, 4)) / G, cache)
    dx2, _, _ = sub.batchnorm_backward(3 * xh / G, cache)
    assert np.allclose(dx1, 0, atol=1e-9) and np.allclose(dx2, 0, atol=1e-8)
