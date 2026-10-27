import numpy as np
import sub

rng = np.random.default_rng(13)
X = rng.normal(size=(12, 3)) @ rng.normal(size=(3, 10)) + 0.05 * rng.normal(size=(12, 10))


def _numgrad(f, P, h=1e-6):
    g = np.zeros_like(P)
    for idx in np.ndindex(P.shape):
        E = np.zeros_like(P)
        E[idx] = h
        g[idx] = (f(P + E) - f(P - E)) / (2 * h)
    return g


def _rel(a, b):
    return np.linalg.norm(a - b) / (np.linalg.norm(a) + np.linalg.norm(b))


def test_grad_U_matches_finite_differences():
    U, V = rng.normal(size=(12, 2)), rng.normal(size=(10, 2))
    dU, _ = sub.grads(U, V, X)
    assert dU.shape == U.shape
    assert _rel(dU, _numgrad(lambda P: sub.loss(P, V, X), U)) < 1e-5


def test_grad_V_matches_finite_differences():
    U, V = rng.normal(size=(12, 2)), rng.normal(size=(10, 2))
    _, dV = sub.grads(U, V, X)
    assert dV.shape == V.shape
    assert _rel(dV, _numgrad(lambda P: sub.loss(U, P, X), V)) < 1e-5


def test_gradient_descent_reaches_eckart_young():
    s = np.linalg.svd(X, compute_uv=False)
    best = np.sqrt(np.sum(s[3:] ** 2))
    U, V = sub.fit(X, 3, steps=4000, lr=0.3 / s[0], seed=0)
    err = np.linalg.norm(X - U @ V.T)
    assert err <= 1.01 * best, f"error {err:.4f}, optimum {best:.4f}"
    assert err >= best - 1e-9, "nothing can beat the truncated SVD"
