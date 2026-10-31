import math
import numpy as np
import sub

rng = np.random.default_rng(5)
x = rng.normal(2.0, 1.5, size=40)


def test_nll_matches_log_density():
    mu, s = 1.0, 0.3
    sig = math.exp(s)
    ref = -np.mean(-0.5 * np.log(2 * np.pi * sig ** 2) - (x - mu) ** 2 / (2 * sig ** 2))
    assert abs(sub.nll(mu, s, x) - ref) < 1e-12


def test_grad_matches_finite_differences():
    for mu, s in [(1.0, 0.3), (2.5, -0.2), (-1.0, 1.1)]:
        g = sub.grad_nll(mu, s, x)
        h = 1e-6
        num = np.array([
            (sub.nll(mu + h, s, x) - sub.nll(mu - h, s, x)) / (2 * h),
            (sub.nll(mu, s + h, x) - sub.nll(mu, s - h, x)) / (2 * h),
        ])
        assert g.shape == (2,)
        assert np.linalg.norm(g - num) / (np.linalg.norm(g) + np.linalg.norm(num)) < 1e-5


def test_gradient_vanishes_at_the_mle():
    m, sd = sub.mle(x)
    assert abs(m - x.mean()) < 1e-12
    assert abs(sd - np.sqrt(np.mean((x - x.mean()) ** 2))) < 1e-12
    assert np.linalg.norm(sub.grad_nll(m, math.log(sd), x)) < 1e-10
