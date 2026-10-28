import numpy as np
import sub

rng = np.random.default_rng(5)
X32 = (np.float32(1e4) + rng.normal(size=1000).astype(np.float32)).astype(np.float32)
TRUE_VAR = float(np.var(X32.astype(np.float64)))


def test_naive_cancels():
    _, v = sub.naive_moments(X32)
    assert abs(float(v) - TRUE_VAR) > 0.3


def test_welford_is_accurate():
    m, v = sub.welford(X32)
    assert abs(float(m) - X32.astype(np.float64).mean()) < 1e-2
    assert abs(float(v) - TRUE_VAR) < 0.01


def test_grad_layernorm_recompute():
    x = rng.normal(size=(4, 6)) * 2 + 1
    g = rng.normal(size=6) + 1
    G = rng.normal(size=(4, 6))
    def f(x, g, b):
        mu = x.mean(axis=1, keepdims=True)
        y = g * (x - mu) / np.sqrt(x.var(axis=1, keepdims=True) + 1e-5) + b
        return float(np.sum(y * G))
    dx, dg, db = sub.layernorm_backward_recompute(G, x, g)
    b0 = np.zeros(6)
    for arr, grad, pos in ((x, dx, 0), (g, dg, 1), (b0, db, 2)):
        num = np.zeros_like(arr)
        for idx in np.ndindex(arr.shape):
            args = [x.copy(), g.copy(), b0.copy()]
            args[pos][idx] += 1e-6
            fp = f(*args)
            args[pos][idx] -= 2e-6
            num[idx] = (fp - f(*args)) / 2e-6
        assert np.allclose(grad, num, atol=1e-6), pos
