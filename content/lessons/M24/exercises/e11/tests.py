import math
import numpy as np
import sub

CASES = [
    (np.square, lambda x: 2 * x, lambda t: t * t + 1, 1.5),
    (np.sin, np.cos, lambda t: math.exp(-0.5) * math.sin(t), 0.7),
]


def test_grad_pathwise_and_score():
    h = 1e-5
    for i, (f, fp, exact, theta) in enumerate(CASES):
        truth = (exact(theta + h) - exact(theta - h)) / (2 * h)
        p, ps = sub.pathwise_grad(fp, theta, 100000, np.random.default_rng(20 + i))
        s, ss = sub.score_grad(f, theta, 100000, np.random.default_rng(30 + i))
        assert abs(p - truth) < 4 * ps and abs(s - truth) < 4 * ss, (p, s, truth)
        assert ps < ss


def test_constant_function():
    est, se = sub.score_grad(lambda x: np.full_like(x, 5.0), 0.3, 50000, np.random.default_rng(40))
    assert abs(est) < 4 * se
    est, se = sub.pathwise_grad(lambda x: np.zeros_like(x), 0.3, 1000, np.random.default_rng(41))
    assert est == 0.0 and se == 0.0
