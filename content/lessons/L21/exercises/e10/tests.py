import numpy as np
import sub


def test_learns_the_task():
    theta, acc = sub.rl_arithmetic(60, 1.0, 8, 0)
    assert theta.shape == (10, 10, 10) and acc > 0.95


def test_kl_holds_the_policy_back():
    _, acc0 = sub.rl_arithmetic(30, 1.0, 8, 1)
    theta, _ = sub.rl_arithmetic(30, 1.0, 8, 1, beta=5.0)
    p = sub.softmax(theta)
    assert p.max(axis=2).mean() < sub.softmax(sub.rl_arithmetic(30, 1.0, 8, 1)[0]).max(axis=2).mean()
