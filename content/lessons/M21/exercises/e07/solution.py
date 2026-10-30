import numpy as np


def simulate(n, switch, seed=0):
    """Fraction of games won."""
    rng = np.random.default_rng(seed)
    wins = 0
    for _ in range(n):
        prize = int(rng.integers(3))
        options = [d for d in (1, 2) if d != prize]
        opened = options[int(rng.integers(len(options)))]
        final = ({1, 2} - {opened}).pop() if switch else 0
        wins += final == prize
    return wins / n


def bayes_switch_win():
    """P(prize behind door 1 | host opens door 2)."""
    prior = np.full(3, 1 / 3)
    lik = np.array([0.5, 1.0, 0.0])
    post = prior * lik / np.sum(prior * lik)
    return float(post[1])
