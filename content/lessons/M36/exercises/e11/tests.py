import numpy as np
import sub


def value(P, R, pi, gamma=0.95):
    Ppi = np.einsum("sa,ast->st", pi, P)
    return np.linalg.solve(np.eye(len(pi)) - gamma * Ppi, np.sum(pi * R, axis=1))


def test_learns_near_optimal():
    P, R = sub.gridworld(4)
    V = np.zeros(16)
    for _ in range(2000):
        V = (R + 0.95 * np.einsum("ast,t->sa", P, V)).max(axis=1)
    learned = value(P, R, sub.policy(sub.train(P)))[0]
    no_base = value(P, R, sub.policy(sub.train(P, use_baseline=False)))[0]
    assert abs(learned - V[0]) < 0.5, (learned, V[0])
    assert no_base < learned - 3, (no_base, learned)
