import numpy as np
import sub

A = np.logspace(-3, 3, 100_000)


def test_newton_accuracy():
    x = sub.newton_cbrt_vec(A, 40)
    assert np.max(np.abs(x - np.cbrt(A)) / np.cbrt(A)) < 1e-15


def test_counts():
    n = sub.steps_to_converge(A, "newton")
    b = sub.steps_to_converge(A, "bisect")
    assert n is not None and b is not None
    assert n < 30 and b > 45 and b > 2 * n
