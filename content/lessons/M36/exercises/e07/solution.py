import numpy as np

MOVES = [(-1, 0), (1, 0), (0, -1), (0, 1)]


# provided
def gridworld(n, slip=0.1):
    S, goal = n * n, n * n - 1
    P = np.zeros((4, S, S))
    R = -np.ones((S, 4))
    for s in range(S):
        if s == goal:
            P[:, s, s] = 1
            R[s] = 0
            continue
        r, c = divmod(s, n)
        for a in range(4):
            for b in range(4):
                dr, dc = MOVES[b]
                t = min(max(r + dr, 0), n - 1) * n + min(max(c + dc, 0), n - 1)
                P[a, s, t] += (1 - slip) * (a == b) + slip / 4
    return P, R


def bellman_backup(P, R, V, gamma):
    """Q(s, a) for the value V."""
    return R + gamma * np.einsum("ast,t->sa", P, V)


def value_iteration(P, R, gamma, tol=1e-10):
    """Optimal value, a greedy policy, and the number of sweeps."""
    V = np.zeros(P.shape[1])
    sweeps = 0
    while True:
        Vn = bellman_backup(P, R, V, gamma).max(axis=1)
        sweeps += 1
        if np.max(np.abs(Vn - V)) < tol:
            return Vn, bellman_backup(P, R, Vn, gamma).argmax(axis=1), sweeps
        V = Vn


def greedy_as_matrix(policy, A):
    """Deterministic policy as a probability array."""
    M = np.zeros((len(policy), A))
    M[np.arange(len(policy)), policy] = 1
    return M
