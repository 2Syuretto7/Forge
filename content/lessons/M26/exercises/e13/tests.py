import numpy as np
import sub

rng = np.random.default_rng(13)
T64 = 1.7e9 + rng.standard_normal(100000)
T32 = (1e4 + rng.standard_normal(100000)).astype(np.float32)


def test_float64():
    assert abs(sub.two_pass_var(T64) - 1) < 0.02
    assert abs(sub.welford_var(T64) - sub.two_pass_var(T64)) < 1e-6
    assert abs(sub.one_pass_var(T64) - sub.two_pass_var(T64)) > 0.01


def test_float32():
    truth = sub.two_pass_var(T32.astype(np.float64))
    assert abs(sub.one_pass_var(T32) - truth) > 0.5
    assert abs(sub.two_pass_var(T32) - truth) < 1e-3


def test_small_example():
    x = np.array([1.0, 2.0, 3.0, 4.0])
    for f in (sub.one_pass_var, sub.two_pass_var, sub.welford_var):
        assert abs(f(x) - 1.25) < 1e-12
