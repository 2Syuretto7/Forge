import numpy as np


def mle_p(k, n):
    return k / n


def smoothed_p(k, n, alpha=1.0):
    return (k + alpha) / (n + 2 * alpha)


def heldout_logloss(p, k_test, n_test):
    """Average negative log-likelihood per held-out flip; inf if an observed outcome had probability 0."""
    total = 0.0
    if k_test > 0:
        if p <= 0:
            return float("inf")
        total -= k_test * np.log(p)
    if n_test - k_test > 0:
        if p >= 1:
            return float("inf")
        total -= (n_test - k_test) * np.log(1 - p)
    return float(total / n_test)


def expected_logloss(estimator, p_true, n_train, n_test, trials, seed=0):
    """Average held-out log-loss of estimator(k, n_train) over simulated datasets."""
    rng = np.random.default_rng(seed)
    total = 0.0
    for _ in range(trials):
        k = rng.binomial(n_train, p_true)
        kt = rng.binomial(n_test, p_true)
        total += heldout_logloss(estimator(k, n_train), kt, n_test)
    return total / trials
