import numpy as np
import sub


def test_grad_top_eigenvalue():
    rng = np.random.default_rng(0)
    G = rng.standard_normal((6, 6))
    S = G + G.T
    D = sub.grad_top_eigenvalue(S)
    h = 1e-6
    for i, j in ((0, 0), (1, 3), (4, 2), (5, 5)):
        E = np.zeros((6, 6))
        E[i, j] = E[j, i] = h
        num = (sub.top_eigenvalue(S + E) - sub.top_eigenvalue(S - E)) / (2 * h)
        assert abs(num - (D[i, j] + D[j, i] if i != j else D[i, i])) < 1e-6


def test_counts_planted_directions():
    rng = np.random.default_rng(1)
    assert sub.count_outliers(sub.planted_matrix(1200, 300, [], rng)) == 0
    assert sub.count_outliers(sub.planted_matrix(1200, 300, [3.0, 5.0, 8.0], rng)) == 3
    assert sub.count_outliers(sub.planted_matrix(1200, 300, [3.0, 0.2], rng)) == 1
