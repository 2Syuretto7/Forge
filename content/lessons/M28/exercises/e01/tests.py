import numpy as np
import sub

CONVEX = [
    (lambda x: float(np.sum(x * x)), 2),
    (lambda x: float(np.sum(np.abs(x))), 3),
    (lambda x: float(np.exp(x[0])), 1),
    (lambda x: float(np.max(x) + np.log(np.sum(np.exp(x - np.max(x))))), 4),
    (lambda x: float(np.linalg.norm(x)), 3),
]


def test_convex_functions_pass():
    for i, (f, d) in enumerate(CONVEX):
        assert sub.search_violation(f, d, 300, np.random.default_rng(i)) <= 1e-12, i
    assert sub.second_difference_min(lambda x: x * x, -3, 3) > 0
    assert sub.second_difference_min(np.abs, -3, 3) >= -1e-15


def test_nonconvex_functions_fail():
    assert sub.search_violation(lambda x: float(np.sin(x[0])), 1, 300, np.random.default_rng(9)) > 0.1
    assert sub.search_violation(lambda x: float(x[0] ** 3), 1, 300, np.random.default_rng(10)) > 0.1
    assert sub.search_violation(lambda x: float(x[0] * x[1]), 2, 300, np.random.default_rng(11)) > 0.1
    assert sub.second_difference_min(lambda x: x**3, -1, 1) < 0


def test_chord_endpoints():
    assert sub.chord_violation(lambda x: float(x[0] ** 2), [0.0], [2.0], [0.0, 1.0]) == 0.0
    assert abs(sub.chord_violation(lambda x: float(x[0] ** 2), [0.0], [2.0], [0.5]) + 1.0) < 1e-12
