import numpy as np


def dpo_loss(lp_c, lp_r, ref_c, ref_r, beta):
    """DPO on n preference pairs: sequence log-probabilities of the chosen and rejected responses
    under the policy (lp_c, lp_r) and the reference (ref_c, ref_r). The loss is the mean of
    -log sigmoid(beta ((lp_c - ref_c) - (lp_r - ref_r))). Return (loss, d_lp_c, d_lp_r)."""
    m = beta * ((lp_c - ref_c) - (lp_r - ref_r))
    loss = np.mean(np.logaddexp(0.0, -m))
    s = 0.5 * (1.0 - np.tanh(m / 2))
    n = len(m)
    return float(loss), -beta * s / n, beta * s / n


def implied_reward(lp, ref, beta):
    """The reward DPO's policy implies for a response: beta times its log-ratio to the reference."""
    return beta * (lp - ref)
