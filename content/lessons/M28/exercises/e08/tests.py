import numpy as np
import sub


def test_closest_point_on_a_line():
    x, lam = sub.solve_equality_qp(np.eye(2), np.zeros(2), [[1.0, 1.0]], [1.0])
    assert np.allclose(x, [0.5, 0.5]) and np.allclose(lam, [-0.5])


def test_plane_and_optimality():
    rng = np.random.default_rng(8)
    M = rng.normal(size=(4, 4))
    A = M @ M.T + np.eye(4)
    b = rng.normal(size=4)
    C = np.array([[1.0, 1.0, 1.0, 1.0], [1.0, -1.0, 0.0, 2.0]])
    d = np.array([1.0, 0.5])
    x, lam = sub.solve_equality_qp(A, b, C, d)
    assert np.allclose(C @ x, d)
    assert np.allclose(A @ x - b + C.T @ lam, 0)
    assert sub.projected_minimum_check(A, b, C, d, x, 200, rng) > 0


def test_multiplier_is_a_sensitivity():
    A, b, C = np.diag([1.0, 3.0]), np.array([1.0, 0.0]), np.array([[1.0, 2.0]])
    h = 1e-6
    fp = sub.objective(A, b, sub.solve_equality_qp(A, b, C, [1.0 + h])[0])
    fm = sub.objective(A, b, sub.solve_equality_qp(A, b, C, [1.0 - h])[0])
    lam = sub.solve_equality_qp(A, b, C, [1.0])[1][0]
    assert abs((fp - fm) / (2 * h) + lam) < 1e-6
