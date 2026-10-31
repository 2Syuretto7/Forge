import numpy as np
import sub

C = 0.7468241328124271


def f(X):
    return np.exp(-np.sum(X * X, axis=1))


def test_one_dimension_grid_wins():
    g = abs(sub.grid_mean(f, 1, 1000) - C)
    m = abs(sub.mc_mean(f, 1, 1000, np.random.default_rng(11)) - C)
    assert g < 1e-7 and m > 100 * g


def test_eight_dimensions_random_points_win():
    g = abs(sub.grid_mean(f, 8, 4) - C**8)
    m = abs(sub.mc_mean(f, 8, 4**8, np.random.default_rng(12)) - C**8)
    assert m < g / 2, (m, g)


def test_shapes():
    assert abs(sub.grid_mean(lambda X: X[:, 0] + X[:, 1], 2, 10) - 1.0) < 1e-12
