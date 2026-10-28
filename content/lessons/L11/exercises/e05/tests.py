import numpy as np
import sub

rng = np.random.default_rng(5)
X = rng.normal(size=(6, 4)) * 2
B = rng.normal(size=4)
DY = rng.normal(size=(6, 4))


def test_grad_gelu():
    x = np.linspace(-4, 4, 41)
    num = (sub.gelu(x + 1e-6) - sub.gelu(x - 1e-6)) / 2e-6
    assert np.allclose(sub.gelu_grad(x), num, atol=1e-8)


def test_grad_fused_bias_gelu():
    f = lambda x, b: float(np.sum(sub.bias_gelu_forward(x, b)[0] * DY))
    _, cache = sub.bias_gelu_forward(X, B)
    dx, db = sub.bias_gelu_backward(DY, cache)
    nx = np.zeros_like(X)
    for idx in np.ndindex(X.shape):
        E = np.zeros_like(X)
        E[idx] = 1e-6
        nx[idx] = (f(X + E, B) - f(X - E, B)) / 2e-6
    nb = np.array([(f(X, B + e) - f(X, B - e)) / 2e-6 for e in np.eye(4) * 1e-6])
    assert np.allclose(dx, nx, atol=1e-7) and np.allclose(db, nb, atol=1e-7)


def test_traffic():
    assert sub.traffic(1000) == 4000 and sub.traffic(1000, fused=False) == 8000
    assert sub.traffic(10, bytes_per=4, fused=False) == 160
