import numpy as np
import sub


def spd(n, seed):
    G = np.random.default_rng(seed).standard_normal((n, n))
    return G @ G.T / n + np.eye(n)


def test_grad_quadratic():
    A, rng = spd(6, 0), np.random.default_rng(1)
    b, x = rng.standard_normal(6), rng.standard_normal(6)
    g = sub.grad_quadratic(A, b, x)
    h = 1e-6
    for i in range(6):
        e = np.zeros(6)
        e[i] = h
        assert abs((sub.quadratic(A, b, x + e) - sub.quadratic(A, b, x - e)) / (2 * h) - g[i]) < 1e-7


def test_solves():
    A = spd(200, 2)
    b = np.random.default_rng(3).standard_normal(200)
    x, norms, dirs = sub.cg(lambda v: A @ v, b)
    assert np.linalg.norm(A @ x - b) <= 1e-9 * np.linalg.norm(b)
    assert abs(norms[0] - np.linalg.norm(b)) < 1e-12 and len(norms) == len(dirs) + 1
    assert len(dirs) < 200


def test_conjugate_directions():
    A = spd(30, 4)
    _, _, dirs = sub.cg(lambda v: A @ v, np.ones(30))
    P = np.array(dirs[:8])
    G = P @ A @ P.T
    off = G - np.diag(np.diag(G))
    assert np.max(np.abs(off)) < 1e-8 * np.max(np.abs(np.diag(G)))
