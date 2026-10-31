import numpy as np
import sub


def test_r_hat_detects_stuck_chains():
    rng = np.random.default_rng(0)
    mixed = sub.run_chains([-1.0, 1.0, -1.0, 1.0], 2.0, 1.0, 5000, rng)
    assert sub.r_hat(mixed) < 1.02
    stuck = sub.run_chains([-5.0, 5.0, -5.0, 5.0], 10.0, 1.0, 5000, rng)
    assert sub.r_hat(stuck) > 2.0
    for c in stuck:
        assert sub.ess(c) > 300
    assert np.all(np.abs(stuck.mean(axis=1)) > 4)
    same = sub.run_chains([-5.0, -5.0, -5.0, -5.0], 10.0, 1.0, 5000, rng)
    assert sub.r_hat(same) < 1.05


def test_r_hat_formula():
    c = np.array([[0.0, 1.0, 2.0], [1.0, 2.0, 3.0]])
    W = 1.0
    B = 3 * np.var([1.0, 2.0], ddof=1)
    assert abs(sub.r_hat(c) - np.sqrt((2 / 3 * W + B / 3) / W)) < 1e-12
