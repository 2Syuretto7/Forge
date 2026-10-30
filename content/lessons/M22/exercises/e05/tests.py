import numpy as np
import sub

rng = np.random.default_rng(5)


def moments(p, v):
    return p @ v, p @ v**2 - (p @ v) ** 2


def test_sum_rule_on_random_tables():
    for _ in range(20):
        J = rng.random((4, 5))
        J /= J.sum()
        xs, ys = rng.normal(size=4), rng.normal(size=5)
        px, py = sub.marginals(J)
        assert abs(px.sum() - 1) < 1e-12 and px.shape == (4,) and py.shape == (5,)
        vx, vy = moments(px, xs)[1], moments(py, ys)[1]
        c = sub.covariance(J, xs, ys)
        assert abs(sub.var_of_sum(J, xs, ys) - (vx + vy + 2 * c)) < 1e-12
        assert -1 - 1e-12 <= sub.correlation(J, xs, ys) <= 1 + 1e-12


def test_independent_table_has_no_covariance():
    px, py = np.array([0.2, 0.5, 0.3]), np.array([0.6, 0.4])
    J = np.outer(px, py)
    xs, ys = np.array([1.0, 2.0, 5.0]), np.array([-1.0, 4.0])
    assert abs(sub.covariance(J, xs, ys)) < 1e-12
    assert abs(sub.var_of_sum(J, xs, ys) - (moments(px, xs)[1] + moments(py, ys)[1])) < 1e-12


def test_perfect_correlation():
    J = np.diag([0.25, 0.25, 0.5])
    v = np.array([0.0, 1.0, 3.0])
    assert abs(sub.correlation(J, v, v) - 1) < 1e-12
    assert abs(sub.correlation(J, v, -2 * v) + 1) < 1e-12
