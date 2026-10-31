import numpy as np
import sub


def test_optimality():
    P, R = sub.gridworld(5)
    V, pol, sweeps = sub.value_iteration(P, R, 0.95)
    assert np.max(np.abs(V - sub.bellman_backup(P, R, V, 0.95).max(axis=1))) < 1e-8
    pi = sub.greedy_as_matrix(pol, 4)
    Ppi = np.einsum("sa,ast->st", pi, P)
    Vpi = np.linalg.solve(np.eye(25) - 0.95 * Ppi, np.sum(pi * R, axis=1))
    assert np.max(np.abs(Vpi - V)) < 1e-6
    assert V[24] == 0 and -9 < V[0] < -7


def test_contraction():
    P, R = sub.gridworld(4)
    Vs, _, _ = sub.value_iteration(P, R, 0.9)
    V = np.zeros(16)
    for _ in range(20):
        Vn = sub.bellman_backup(P, R, V, 0.9).max(axis=1)
        assert np.max(np.abs(Vn - Vs)) <= 0.9 * np.max(np.abs(V - Vs)) + 1e-12
        V = Vn
