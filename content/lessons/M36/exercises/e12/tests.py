import numpy as np
import sub


def test_baseline_reduces_variance():
    P, R = sub.gridworld(5)
    rng = np.random.default_rng(0)
    for theta in (np.zeros((25, 4)), np.tile([0.0, 1.0, 0.0, 1.0], (25, 1))):
        without, with_b, gap = sub.variance_reduction(P, R, theta, 0.95, 400, rng)
        assert without > 3 * with_b, (without, with_b)
        assert gap < 4 * np.sqrt(without / 400)
