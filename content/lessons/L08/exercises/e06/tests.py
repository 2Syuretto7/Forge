import numpy as np
import sub

rng = np.random.default_rng(6)


def _num(f, x, h=1e-6):
    g = np.zeros_like(x)
    for idx in np.ndindex(x.shape):
        e = np.zeros_like(x)
        e[idx] = h
        g[idx] = (f(x + e) - f(x - e)) / (2 * h)
    return g


X = rng.uniform(0.5, 2.0, size=(3, 4)) * rng.choice([-1.0, 1.0], size=(3, 4))
P = np.abs(X)
G = rng.normal(size=(3, 4))

CASES = {
    "exp": (lambda t: t.exp(), np.exp, X),
    "log": (lambda t: t.log(), np.log, P),
    "relu": (lambda t: t.relu(), lambda x: np.maximum(x, 0), X),
    "tanh": (lambda t: t.tanh(), np.tanh, X),
    "pow": (lambda t: t ** 3, lambda x: x ** 3, X),
    "neg": (lambda t: -t, lambda x: -x, X),
    "sub": (lambda t: t - 2.5, lambda x: x - 2.5, X),
    "rsub": (lambda t: 1.0 - t, lambda x: 1.0 - x, X),
    "div": (lambda t: t / 3.0, lambda x: x / 3.0, X),
    "rdiv": (lambda t: 1.0 / t, lambda x: 1.0 / x, P),
}


def test_forward_values():
    for name, (op, ref, x) in CASES.items():
        assert np.allclose(op(sub.Tensor(x)).data, ref(x)), name


def test_grad_each_operation():
    for name, (op, ref, x) in CASES.items():
        t = sub.Tensor(x)
        (op(t) * sub.Tensor(G)).sum().backward()
        assert t.grad is not None, name
        assert np.allclose(t.grad, _num(lambda v: np.sum(G * ref(v)), x), atol=1e-5), name


def test_grad_mean():
    t = sub.Tensor(X)
    (t.mean(axis=0) * sub.Tensor(G[0])).sum().backward()
    assert np.allclose(t.grad, np.tile(G[0] / 3, (3, 1)))
    u = sub.Tensor(X)
    u.mean().backward()
    assert np.allclose(u.grad, np.full_like(X, 1 / 12))


def test_grad_tensor_division():
    a, b = sub.Tensor(X), sub.Tensor(P)
    ((a / b) * sub.Tensor(G)).sum().backward()
    assert np.allclose(a.grad, G / P)
    assert np.allclose(b.grad, -G * X / P ** 2)
