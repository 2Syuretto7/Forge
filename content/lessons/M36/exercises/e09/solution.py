import numpy as np


def train_bandit(means, steps, lr, use_baseline, rng, noise=1.0):
    """REINFORCE on a Gaussian bandit; returns the final arm probabilities."""
    K = len(means)
    z = np.zeros(K)
    b = 0.0
    for _ in range(steps):
        p = np.exp(z - z.max())
        p /= p.sum()
        a = rng.choice(K, p=p)
        r = means[a] + noise * rng.standard_normal()
        g = -p
        g[a] += 1
        z += lr * (r - (b if use_baseline else 0.0)) * g
        if use_baseline:
            b += 0.05 * (r - b)
    p = np.exp(z - z.max())
    return p / p.sum()


def best_arm_prob(probs, means):
    """Probability on the arm with the highest mean."""
    return float(probs[int(np.argmax(means))])
