import numpy as np
import sub


def test_exact_at_knots_and_linear_between():
    t = np.array([0.0, 1.0, 3.0, 4.0])
    v = np.array([1.0, 3.0, 2.0, 5.0])
    p = sub.hinge_network(t, v)
    assert np.allclose(sub.evaluate(p, t), v)
    assert np.allclose(sub.evaluate(p, [0.5, 2.0, 3.5]), [2.0, 2.5, 3.5])
    assert len(p[0]) == 3, "one unit per piece"


def test_error_bound_and_quadratic_convergence():
    f = lambda x: np.sin(np.pi * x)  # noqa: E731
    e20 = sub.max_error(f, 20)
    e40 = sub.max_error(f, 40)
    assert e20 <= np.pi ** 2 * 0.1 ** 2 / 8 + 1e-12
    assert 3.5 < e20 / e40 < 4.5
