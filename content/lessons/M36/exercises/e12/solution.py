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


# provided
def policy(theta):
    e = np.exp(theta - theta.max(axis=1, keepdims=True))
    return e / e.sum(axis=1, keepdims=True)


# provided
def run_episode(P, pi, rng, max_steps=60):
    S = P.shape[1]
    s, traj = 0, []
    for _ in range(max_steps):
        if s == S - 1:
            break
        a = rng.choice(4, p=pi[s])
        traj.append((s, a, -1.0))
        s = rng.choice(S, p=P[a, s])
    return traj


def episode_gradient(theta, traj, gamma, V=None):
    """REINFORCE gradient estimate from one episode."""
    pi = policy(theta)
    g = np.zeros_like(theta)
    G = 0.0
    for s, a, r in reversed(traj):
        G = r + gamma * G
        e = -pi[s].copy()
        e[a] += 1
        g[s] += (G - (V[s] if V is not None else 0.0)) * e
    return g


def variance_reduction(P, R, theta, gamma, n, rng):
    """Total variance of the estimates without and with the value baseline."""
    pi = policy(theta)
    Ppi = np.einsum("sa,ast->st", pi, P)
    V = np.linalg.solve(np.eye(len(pi)) - gamma * Ppi, np.sum(pi * R, axis=1))
    trajs = [run_episode(P, pi, rng) for _ in range(n)]
    A = np.array([episode_gradient(theta, t, gamma).ravel() for t in trajs])
    B = np.array([episode_gradient(theta, t, gamma, V).ravel() for t in trajs])
    return float(A.var(axis=0).sum()), float(B.var(axis=0).sum()), float(np.max(np.abs(A.mean(axis=0) - B.mean(axis=0))))
