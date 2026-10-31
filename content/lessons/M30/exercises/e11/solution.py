import numpy as np


# provided
def make_rewards(seed=0):
    return np.random.default_rng(seed).standard_normal(10**6)


def entropy(p):
    """Entropy in nats."""
    p = np.asarray(p, dtype=float)
    q = p[p > 0]
    return float(-np.sum(q * np.log(q)))


def effective_actions(p):
    """exp(entropy)."""
    return float(np.exp(entropy(p)))


def sweep(r, taus):
    """Entropy and expected reward of the Gibbs distribution at each temperature."""
    r = np.asarray(r, dtype=float)
    m = r.max()
    H, ER = [], []
    for tau in taus:
        e = np.exp((r - m) / tau)
        Z = e.sum()
        p = e / Z
        er = float(p @ r)
        H.append(float(np.log(Z) - (er - m) / tau))
        ER.append(er)
    return np.array(H), np.array(ER)
