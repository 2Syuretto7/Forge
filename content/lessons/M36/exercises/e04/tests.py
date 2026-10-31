import numpy as np
import sub


def test_both_unbiased_reparam_quieter():
    rng = np.random.default_rng(0)
    mu, sigma = 1.5, 0.7
    R = sub.reparam_samples(lambda x: 2 * x, mu, sigma, 200000, rng)
    S = sub.score_samples(lambda x: x**2, mu, sigma, 200000, rng)
    g = sub.exact_grad_square(mu, sigma)
    assert np.max(np.abs(R.mean(axis=0) - g)) < 0.02
    assert np.max(np.abs(S.mean(axis=0) - g)) < 0.06
    assert np.all(S.var(axis=0) > 5 * R.var(axis=0))
