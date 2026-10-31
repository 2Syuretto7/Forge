import numpy as np
import sub

rng = np.random.default_rng(5)


def _num(f, x, h=1e-6):
    g = np.zeros_like(x)
    for idx in np.ndindex(x.shape):
        e = np.zeros_like(x)
        e[idx] = h
        g[idx] = (f(x + e) - f(x - e)) / (2 * h)
    return g


def test_forward():
    A = sub.Tensor(rng.normal(size=(3, 4)))
    B = sub.Tensor(rng.normal(size=(4, 2)))
    assert np.allclose((A @ B).data, A.data @ B.data)
    assert A.T.shape == (4, 3)
    assert A.reshape(2, 6).shape == (2, 6)


def test_grad_matmul():
    A = rng.normal(size=(3, 4))
    B = rng.normal(size=(4, 2))
    G = rng.normal(size=(3, 2))
    tA, tB = sub.Tensor(A), sub.Tensor(B)
    ((tA @ tB) * sub.Tensor(G)).sum().backward()
    assert np.allclose(tA.grad, _num(lambda x: np.sum(G * (x @ B)), A), atol=1e-6)
    assert np.allclose(tB.grad, _num(lambda x: np.sum(G * (A @ x)), B), atol=1e-6)


def test_grad_transpose_reshape():
    A = rng.normal(size=(3, 4))
    G1 = rng.normal(size=(4, 3))
    G2 = rng.normal(size=(6, 2))
    tA = sub.Tensor(A)
    ((tA.T * sub.Tensor(G1)).sum() + (tA.reshape(6, 2) * sub.Tensor(G2)).sum()).backward()
    f = lambda x: np.sum(G1 * x.T) + np.sum(G2 * x.reshape(6, 2))
    assert np.allclose(tA.grad, _num(f, A), atol=1e-6)


def test_grad_linear_layer():
    X = rng.normal(size=(5, 3))
    W = rng.normal(size=(3, 2))
    b = rng.normal(size=2)
    G = rng.normal(size=(5, 2))
    tX, tW, tb = sub.Tensor(X), sub.Tensor(W), sub.Tensor(b)
    ((tX @ tW + tb) * sub.Tensor(G)).sum().backward()
    assert np.allclose(tW.grad, X.T @ G)
    assert np.allclose(tb.grad, G.sum(axis=0))
    assert np.allclose(tX.grad, G @ W.T)
