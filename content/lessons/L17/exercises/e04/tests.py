import numpy as np
import sub

V = [0.01] * 10000


def test_naive_stalls():
    s = sub.naive_sum(V, np.float16)
    assert isinstance(s, np.float16) and float(s) == 32.0


def test_repairs():
    assert abs(float(sub.kahan_sum(V, np.float16)) - 100) < 0.1
    assert abs(float(sub.wide_accumulator_sum(V, np.float16)) - 100) < 0.1
    assert abs(float(sub.naive_sum(V, np.float32)) - 100) < 0.01
