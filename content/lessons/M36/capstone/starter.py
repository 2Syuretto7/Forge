import numpy as np

GAMMA = 0.95
MOVES = [(-1, 0), (1, 0), (0, -1), (0, 1)]


# provided
def make_world(n=5, slip=0.1):
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


def train(episodes=800, lr=0.1, seed=0):
    """REINFORCE with returns-to-go and a learned state-value baseline."""
    raise NotImplementedError


def episode_gradient(theta, traj, V=None):
    """REINFORCE gradient estimate from one episode."""
    raise NotImplementedError


def gradient_variance(theta, V, n=400, seed=1):
    """Total variance of gradient estimates without and with the learned baseline."""
    raise NotImplementedError


def optimal_value():
    """V* at the start state by value iteration."""
    raise NotImplementedError


# your answer
REPORT = """
"""
