import numpy as np
import sub


def test_grad_score():
    h = 1e-6
    for theta in (-1.5, 0.0, 0.8):
        for x in (0, 1):
            num = (sub.log_prob(x, theta + h) - sub.log_prob(x, theta - h)) / (2 * h)
            assert abs(num - sub.score(x, theta)) < 1e-8


def test_estimate_converges():
    rng = np.random.default_rng(0)
    for theta in (-1.0, 0.5):
        est = sub.estimate_grad(theta, 3.0, 1.0, 200000, rng)
        assert abs(est - sub.exact_grad(theta, 3.0, 1.0)) < 0.01
