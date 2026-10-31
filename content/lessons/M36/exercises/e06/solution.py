import bisect
import numpy as np


def discounted_return(rewards, gamma):
    """Sum of gamma^t r_t."""
    return float(sum(r * gamma**t for t, r in enumerate(rewards)))


def chain_of(P, R, pi):
    """Transition matrix and expected reward of the chain a policy induces."""
    return np.einsum("sa,ast->st", pi, P), np.sum(pi * R, axis=1)


def policy_evaluation(P, R, pi, gamma):
    """Exact value of a policy."""
    Ppi, Rpi = chain_of(P, R, pi)
    return np.linalg.solve(np.eye(len(Rpi)) - gamma * Ppi, Rpi)


def mc_value(P, R, pi, gamma, s0, episodes, horizon, rng):
    """Monte Carlo estimate of V(s0)."""
    cpi = np.cumsum(pi, axis=1).tolist()
    cP = np.cumsum(P, axis=2).tolist()
    Rl = R.tolist()
    last_a, last_s = pi.shape[1] - 1, P.shape[1] - 1
    u = rng.random((episodes, horizon, 2)).tolist()
    total = 0.0
    for e in range(episodes):
        s, g, disc = s0, 0.0, 1.0
        for ua, us in u[e]:
            a = min(bisect.bisect_right(cpi[s], ua), last_a)
            g += disc * Rl[s][a]
            disc *= gamma
            s = min(bisect.bisect_right(cP[a][s], us), last_s)
        total += g
    return total / episodes
