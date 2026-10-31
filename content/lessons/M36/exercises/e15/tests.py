import numpy as np
import sub


def test_intermediate_beta_wins():
    rng = np.random.default_rng(0)
    r = rng.standard_normal(20)
    r_hat = r + 0.3 * rng.standard_normal(20)
    worst = int(np.argmin(r))
    r_hat[worst] = r.max() + 0.2
    pi_ref = np.ones(20) / 20
    betas = [0.01, 0.5, 1.0, 100.0]
    res = sub.sweep(pi_ref, r_hat, r, betas)
    rewards = [x[0] for x in res]
    kls = [x[1] for x in res]
    assert rewards[0] < sub.true_reward(pi_ref, r) - 1
    assert max(rewards[1:3]) > max(rewards[0], rewards[3]) + 0.1
    assert kls[0] > kls[1] > kls[2] > kls[3] >= 0
