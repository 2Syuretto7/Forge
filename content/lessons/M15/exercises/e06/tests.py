import math
import sub


def test_limits():
    assert abs(sub.exp_quotient(1e-6) - 1) < 1e-6
    assert abs(sub.sin_quotient(1e-4) - 1) < 1e-8
    assert abs(sub.log_slope(4.0, 1e-7) - 0.25) < 1e-7


def test_orders():
    assert abs(sub.order_of_error(sub.exp_quotient, 1.0, 1e-3) - 2) < 0.01
    assert abs(sub.order_of_error(sub.sin_quotient, 1.0, 1e-2) - 4) < 0.01


def test_expm1():
    assert abs(math.expm1(1e-12) / 1e-12 - 1) < 1e-12
    assert abs(sub.exp_quotient(1e-12) - 1) > 1e-6
