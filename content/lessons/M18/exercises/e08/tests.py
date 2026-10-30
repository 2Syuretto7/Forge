import numpy as np
import sub

rng = np.random.default_rng(8)
M = rng.normal(size=(5, 5))
S = M + M.T
w, V = np.linalg.eigh(S)


def test_grad_matches_finite_differences():
    x = rng.normal(size=5)
    g = sub.rayleigh_grad(S, x)
    n = np.zeros(5)
    for i in range(5):
        e = np.zeros(5)
        e[i] = 1e-6
        n[i] = (sub.rayleigh(S, x + e) - sub.rayleigh(S, x - e)) / 2e-6
    assert np.linalg.norm(g - n) / (np.linalg.norm(g) + np.linalg.norm(n)) < 1e-6


def test_grad_vanishes_at_eigenvectors():
    for i in range(5):
        assert np.linalg.norm(sub.rayleigh_grad(S, V[:, i])) < 1e-10


def test_ascent():
    P = S + 10 * np.eye(5)
    x = sub.ascend(P, rng.normal(size=5), lr=1.0 / np.max(np.abs(w + 10)), steps=2000)
    assert abs(abs(x @ V[:, -1]) - 1) < 1e-6
