import math
import sub


def rel(a, b):
    return abs(a - b) / abs(b)


def test_one_minus_cos():
    naive, stable = sub.one_minus_cos(1e-8)
    assert naive == 0.0
    assert rel(stable, 5e-17) < 1e-12


def test_expm1():
    naive, stable = sub.expm1_over_x(1e-12)
    assert rel(naive, 1.0) > 1e-5
    assert rel(stable, 1 + 5e-13) < 1e-15


def test_small_root():
    naive, stable = sub.small_root(1.0, -1e8, 1.0)
    assert rel(stable, 1e-8) < 1e-15
    assert rel(naive, 1e-8) > 0.1
    n2, s2 = sub.small_root(2.0, 3.0, -2.0)
    assert abs(s2 - 0.5) < 1e-15 and abs(n2 - 0.5) < 1e-15
