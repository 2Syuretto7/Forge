import numpy as np
import sub


def f(x):
    return float(np.sum(np.logaddexp(0.0, x)) + 0.5 * np.sum(np.diff(x) ** 2))


def grad(x):
    d = np.diff(x)
    return 1 / (1 + np.exp(-x)) + np.concatenate([[0.0], d]) - np.concatenate([d, [0.0]])


def test_grad_random_directions():
    x = np.random.default_rng(3).normal(size=10000)
    assert sub.directional_check(f, grad, x) < 1e-7
    assert sub.directional_check(f, sub.buggy_grad(grad, 1234), x) > 1e-4
