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
    raise NotImplementedError


def run_episode(P, pi, rng, max_steps=50):
    """One episode from state 0 to the goal."""
    raise NotImplementedError


def train(P, gamma=0.95, episodes=600, lr=0.1, use_baseline=True, seed=0):
    """REINFORCE with returns-to-go and an optional learned baseline."""
    raise NotImplementedError
