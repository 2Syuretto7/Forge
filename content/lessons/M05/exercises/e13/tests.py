import numpy as np
import sub


def test_small_case_agrees():
    t = sub.terms(10)
    assert abs(sub.forward(t) - sub.backward(t)) < 1e-6


def test_backward_is_much_better():
    fwd, bwd = sub.errors(1_000_000)
    assert fwd > 1e-4, fwd
    assert bwd < 1e-6, bwd
    assert fwd > 100 * bwd


def test_close_to_pi_squared_over_six():
    t = sub.terms(1_000_000)
    tail = 1 / 1_000_000  # the terms beyond n sum to about 1/n
    assert abs(sub.backward(t) + tail - np.pi ** 2 / 6) < 1e-5
