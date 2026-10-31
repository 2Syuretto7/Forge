import numpy as np
import sub


def test_dpo_recovers_optimum():
    rng = np.random.default_rng(0)
    K, beta = 8, 0.5
    r = rng.standard_normal(K)
    ref = np.log(np.ones(K) / K)
    N = sub.sample_preferences(r, 20000, rng)
    z = sub.train_dpo(ref, N, beta)
    p = np.exp(z - z.max())
    p /= p.sum()
    target = np.exp(ref + r / beta)
    target /= target.sum()
    assert sub.tv(p, target) < 0.05
