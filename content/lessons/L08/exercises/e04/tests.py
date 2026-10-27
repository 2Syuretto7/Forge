import numpy as np
import sub

rng = np.random.default_rng(4)


def _num(f, x, h=1e-6):
    g = np.zeros_like(x)
    for idx in np.ndindex(x.shape):
        e = np.zeros_like(x)
        e[idx] = h
        g[idx] = (f(x + e) - f(x - e)) / (2 * h)
    return g


def test_forward_values():
    a = sub.Tensor(rng.normal(size=(3, 4)))
    b = sub.Tensor(rng.normal(size=4))
    assert np.allclose((a + b).data, a.data + b.data)
    assert np.allclose((a * b).data, a.data * b.data)
    assert np.allclose(a.sum(axis=0).data, a.data.sum(axis=0))


def test_grad_add_mul_broadcast():
    A = rng.normal(size=(5, 3))
    b = rng.normal(size=3)
    s = rng.normal(size=(5, 1))
    G = rng.normal(size=(5, 3))

    def f(A, b, s):
        return float(np.sum(G * ((A + b) * s)))

    tA, tb, ts = sub.Tensor(A), sub.Tensor(b), sub.Tensor(s)
    (((tA + tb) * ts) * sub.Tensor(G)).sum().backward()
    assert tb.grad.shape == (3,) and ts.grad.shape == (5, 1)
    assert np.allclose(tA.grad, _num(lambda x: f(x, b, s), A), atol=1e-6)
    assert np.allclose(tb.grad, _num(lambda x: f(A, x, s), b), atol=1e-6)
    assert np.allclose(ts.grad, _num(lambda x: f(A, b, x), s), atol=1e-6)


def test_grad_sum_axis():
    A = rng.normal(size=(4, 3))
    w = rng.normal(size=3)
    tA = sub.Tensor(A)
    (tA.sum(axis=0) * sub.Tensor(w)).sum().backward()
    assert np.allclose(tA.grad, np.tile(w, (4, 1)))
    tB = sub.Tensor(A)
    (tB.sum(axis=1, keepdims=True) * sub.Tensor(np.arange(4.0)[:, None])).sum().backward()
    assert np.allclose(tB.grad, np.tile(np.arange(4.0)[:, None], (1, 3)))


def test_reuse_accumulates():
    x = sub.Tensor(np.array([1.0, -2.0, 3.0]))
    (x * x + x).sum().backward()
    assert np.allclose(x.grad, 2 * x.data + 1)


def test_backward_twice_accumulates_on_leaves():
    x = sub.Tensor(np.array([1.0, 2.0]))
    loss = (x * x).sum()
    loss.backward()
    loss.backward()
    assert np.allclose(x.grad, 4 * x.data)


def test_deep_chain_no_recursion_error():
    x = sub.Tensor(np.array([1.0]))
    y = x
    for _ in range(3000):
        y = y * 1.0001
    y.sum().backward()
    assert np.allclose(x.grad, 1.0001 ** 3000)
