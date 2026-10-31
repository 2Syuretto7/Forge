import numpy as np
import sub

rng = np.random.default_rng(4)
M = rng.normal(size=(3, 3))
Q = M @ M.T + np.eye(3)
C = rng.normal(size=3) * 3
A = rng.normal(size=(4, 3))
B = rng.uniform(0.1, 1.0, size=4)


def test_grad_dual():
    lam = rng.uniform(0, 1, size=4)
    g = sub.dual_grad(Q, C, A, B, lam)
    h = 1e-6
    for j in range(4):
        e = np.zeros(4)
        e[j] = h
        num = (sub.dual_value(Q, C, A, B, lam + e) - sub.dual_value(Q, C, A, B, lam - e)) / (2 * h)
        assert abs(num - g[j]) < 1e-6


def test_weak_and_strong_duality():
    step = 1 / np.linalg.eigvalsh(A @ np.linalg.solve(Q, A.T))[-1]
    lam, x = sub.dual_ascent(Q, C, A, B, step, 20000)
    assert np.all(A @ x <= B + 1e-6)
    p = sub.primal_value(Q, C, x)
    d = sub.dual_value(Q, C, A, B, lam)
    assert abs(p - d) < 1e-6 * max(1, abs(p))
    for _ in range(20):
        l2 = rng.uniform(0, 3, size=4)
        assert sub.dual_value(Q, C, A, B, l2) <= p + 1e-9
