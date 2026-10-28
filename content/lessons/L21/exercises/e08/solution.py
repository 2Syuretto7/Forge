import numpy as np


def dpo_loss(lw, ll, lw_ref, ll_ref, beta):
    """Mean over pairs of -log sigmoid(beta ((lw - lw_ref) - (ll - ll_ref))), with lw, ll the
    policy's log probabilities of the preferred and rejected responses and lw_ref, ll_ref the
    reference's. Return (loss, gradient with respect to lw, gradient with respect to ll)."""
    z = beta * ((lw - lw_ref) - (ll - ll_ref))
    loss = np.mean(np.logaddexp(0, -z))
    s = 1 / (1 + np.exp(z))
    n = len(z)
    return float(loss), -beta * s / n, beta * s / n


def tabular_dpo(ref, prefs, beta, steps=3000, lr=0.5):
    """A policy over K responses, pi = softmax(theta) with theta initialized to log(ref). prefs is
    a list of (winner, loser, count). Gradient descent on the count-weighted DPO loss through the
    log-softmax. Return the final pi."""
    theta = np.log(np.asarray(ref, dtype=float))
    lref = np.log(ref)
    total = sum(c for _, _, c in prefs)
    for _ in range(steps):
        logpi = theta - np.log(np.exp(theta - theta.max()).sum()) - theta.max()
        g_logpi = np.zeros_like(theta)
        for w, l, c in prefs:
            z = beta * ((logpi[w] - lref[w]) - (logpi[l] - lref[l]))
            s = 1 / (1 + np.exp(z))
            g_logpi[w] -= c * beta * s / total
            g_logpi[l] += c * beta * s / total
        pi = np.exp(logpi)
        theta -= lr * (g_logpi - pi * g_logpi.sum())
    return np.exp(theta - theta.max()) / np.exp(theta - theta.max()).sum()
