import numpy as np
import sub

rng = np.random.default_rng(8)
M = rng.normal(size=(5, 5))
S = M + M.T
w, V = np.linalg.eigh(S)


def _numgrad(f, x, h=1e-6):
    g = np.zeros_like(x)
    for i in range(x.size):
        e = np.zeros_like(x)
        e[i] = h
        g[i] = (f(x + e) - f(x - e)) / (2 * h)
    return g


def test_value_and_scale_invariance():
    x = rng.normal(size=5)
    assert abs(sub.rayleigh(S, x) - x @ S @ x / (x @ x)) < 1e-12
    assert abs(sub.rayleigh(S, -3.5 * x) - sub.rayleigh(S, x)) < 1e-12


def test_grad_matches_finite_differences():
    x = rng.normal(size=5)
    g = sub.rayleigh_grad(S, x)
    n = _numgrad(lambda z: sub.rayleigh(S, z), x)
    rel = np.linalg.norm(g - n) / (np.linalg.norm(g) + np.linalg.norm(n))
    assert rel < 1e-5, f"relative error {rel:.2e}"


def test_grad_vanishes_at_eigenvectors():
    for i in range(5):
        assert np.linalg.norm(sub.rayleigh_grad(S, V[:, i])) < 1e-10


def test_bounded_by_extreme_eigenvalues():
    for _ in range(100):
        r = sub.rayleigh(S, rng.normal(size=5))
        assert w[0] - 1e-12 <= r <= w[-1] + 1e-12


def test_ascent_reaches_top_eigenvector():
    P = S + 10 * np.eye(5)  # shift so the top eigenvalue is also largest in magnitude
    x = sub.ascend(P, rng.normal(size=5), lr=1.0 / np.max(np.abs(w + 10)), steps=2000)
    assert abs(abs(x @ V[:, -1]) - 1) < 1e-6
