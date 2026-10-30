import numpy as np
import sub

rng = np.random.default_rng(1)


def numgrad(f, x, h=1e-6):
    g = np.zeros_like(x)
    for i in range(x.size):
        e = np.zeros_like(x)
        e[i] = h
        g[i] = (f(x + e) - f(x - e)) / (2 * h)
    return g


def rel(a, b):
    return np.linalg.norm(a - b) / max(np.linalg.norm(a) + np.linalg.norm(b), 1e-12)


def test_grad_all_four():
    A = rng.normal(size=(5, 5))
    for _ in range(5):
        v = rng.normal(size=2)
        assert rel(sub.grad_f1(v), numgrad(sub.f1, v)) < 1e-8
        x = rng.normal(size=5)
        assert rel(sub.grad_f2(x), numgrad(lambda z: z @ z, x)) < 1e-8
        assert rel(sub.grad_f3(x), numgrad(lambda z: np.log(np.sum(np.exp(z))), x)) < 1e-8
        assert rel(sub.grad_f4(x, A), numgrad(lambda z: 0.5 * z @ A @ z, x)) < 1e-8


def test_values():
    assert np.allclose(sub.grad_f1(np.array([1.0, 2.0])), [4, 1 + np.cos(2)])
    assert np.isclose(sub.grad_f3(np.array([1000.0, 1000.0])).sum(), 1)
