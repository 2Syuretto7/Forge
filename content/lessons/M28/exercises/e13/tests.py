import numpy as np
import sub

A = np.diag([1.0, 10.0])
L = 10.0


def test_threshold():
    assert abs(sub.largest_stable_step(A) - 0.2) < 1e-12
    assert sub.growth_factor(A, 1.9 / L) < 1 < sub.growth_factor(A, 2.1 / L)


def test_divergence_along_the_steep_direction():
    good = sub.gd_path(A, [1.0, 1.0], 1.9 / L, 60)
    bad = sub.gd_path(A, [1.0, 1.0], 2.1 / L, 60)
    assert abs(good[-1, 1]) < 0.05 and abs(bad[-1, 1]) > 100
    assert np.all(np.sign(bad[1:, 1]) != np.sign(bad[:-1, 1]))
    assert abs(good[-1, 0]) < 1e-3 and abs(bad[-1, 0]) < 1e-3
