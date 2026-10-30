import numpy as np
import sub


def test_shell():
    assert sub.shell_fraction(100, 0.05) > 0.99
    assert abs(sub.shell_fraction(2, 0.5) - 0.75) < 1e-15


def test_samples():
    for n in (2, 10, 100):
        assert abs(sub.mean_radius(n) - n / (n + 1)) < 0.003
    P = sub.sample_ball(2, 200_000, seed=4)
    assert abs(np.mean(np.linalg.norm(P, axis=1) < 0.5) - 0.25) < 0.005
