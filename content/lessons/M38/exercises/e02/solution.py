import numpy as np


def bt_prob(r, i, j):
    """Bradley-Terry probability that i beats j."""
    return float(1 / (1 + np.exp(-(r[i] - r[j]))))


def bt_loglik(r, pairs):
    """Log-likelihood of observed (winner, loser) pairs."""
    P = np.asarray(pairs)
    d = np.asarray(r)[P[:, 0]] - np.asarray(r)[P[:, 1]]
    return float(-np.sum(np.logaddexp(0, -d)))


def grad_bt_loglik(r, pairs):
    """Gradient of the log-likelihood in the rewards."""
    P = np.asarray(pairs)
    d = np.asarray(r)[P[:, 0]] - np.asarray(r)[P[:, 1]]
    w = 1 / (1 + np.exp(d))
    g = np.zeros(len(r))
    np.add.at(g, P[:, 0], w)
    np.add.at(g, P[:, 1], -w)
    return g


def count_matrix(pairs, K):
    """N[i, j] = number of times i beat j."""
    N = np.zeros((K, K))
    for i, j in pairs:
        N[i, j] += 1
    return N
