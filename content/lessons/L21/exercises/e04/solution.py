import numpy as np


def gae(rewards, values, gamma, lam):
    """Generalized advantage estimates for one episode. values has one more entry than rewards (the
    value after the last step, 0 at the end of an episode). delta_t = r_t + gamma V_{t+1} - V_t and
    A_t = delta_t + gamma lam A_{t+1}."""
    T = len(rewards)
    adv = np.zeros(T)
    run = 0.0
    for t in reversed(range(T)):
        delta = rewards[t] + gamma * values[t + 1] - values[t]
        run = delta + gamma * lam * run
        adv[t] = run
    return adv


def returns(rewards, gamma):
    """Discounted returns G_t = r_t + gamma G_{t+1}."""
    out = np.zeros(len(rewards))
    run = 0.0
    for t in reversed(range(len(rewards))):
        run = rewards[t] + gamma * run
        out[t] = run
    return out
