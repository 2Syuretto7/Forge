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


def policy(theta):
    """Row-wise softmax."""
    e = np.exp(theta - theta.max(axis=1, keepdims=True))
    return e / e.sum(axis=1, keepdims=True)


def run_episode(P, pi, rng, max_steps=50):
    """One episode from state 0 to the goal."""
    S = P.shape[1]
    s, traj = 0, []
    for _ in range(max_steps):
        if s == S - 1:
            break
        a = rng.choice(4, p=pi[s])
        traj.append((s, a, -1.0))
        s = rng.choice(S, p=P[a, s])
    return traj


def train(P, gamma=0.95, episodes=600, lr=0.1, use_baseline=True, seed=0):
    """REINFORCE with returns-to-go and an optional learned baseline."""
    rng = np.random.default_rng(seed)
    theta = np.zeros((P.shape[1], 4))
    V = np.zeros(P.shape[1])
    for _ in range(episodes):
        pi = policy(theta)
        G = 0.0
        for s, a, r in reversed(run_episode(P, pi, rng)):
            G = r + gamma * G
            b = V[s] if use_baseline else 0.0
            if use_baseline:
                V[s] += 0.1 * (G - V[s])
            g = -pi[s].copy()
            g[a] += 1
            theta[s] += lr * (G - b) * g
    return theta
