import numpy as np
import sub

f = lambda v: v[0] ** 2 + v[1] ** 2 - 3 * v[0] * v[1]  # noqa: E731
H = np.array([[2.0, -3.0], [-3.0, 2.0]])


def test_disguise():
    assert sub.axis_check(f, [0.0, 0.0])
    w, _ = sub.hessian_eigen(H)
    assert np.allclose(w, [-1, 5])
    u = sub.escape_direction(H)
    assert abs(abs(u[0]) - abs(u[1])) < 1e-12
    assert f(0.1 * u) < 0
    assert sub.escape_direction(np.eye(2)) is None
