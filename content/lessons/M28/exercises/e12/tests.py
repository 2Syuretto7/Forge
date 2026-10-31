import numpy as np
import sub


def test_scales():
    H = sub.scaled_least_squares(5000, [0.01, 1.0, 100.0], 12)
    assert sub.kappa(H) > 1e7
    assert sub.kappa(sub.jacobi(H)) < 1.2
    assert np.allclose(np.diag(sub.jacobi(H)), 1)


def test_correlations_are_not_scales():
    A = np.array([[1.0, 0.99], [0.99, 1.0]])
    assert abs(sub.kappa(A) - 199) < 1e-6
    assert abs(sub.kappa(sub.jacobi(A)) - 199) < 1e-6
