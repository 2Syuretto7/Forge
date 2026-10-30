import math
import sub


def test_values_and_bounds():
    assert abs(sub.taylor_sin(0.1, 2) - (0.1 - 0.001 / 6)) < 1e-17
    for x in (0.1, 0.5, 1.0, 2.0):
        for n in range(1, 8):
            assert abs(sub.taylor_sin(x, n) - math.sin(x)) <= sub.sin_bound(x, n) + 1e-16
    assert abs(sub.taylor_exp(1.0, 18) - math.e) < 1e-15


def test_terms_for():
    assert sub.terms_for(0.1, 1e-10) == 3
    assert sub.terms_for(1.0, 1e-15) == 9


def test_grad_series_derivative_is_cosine_series():
    h = 1e-5
    for x in (0.2, 0.9, 1.7):
        for n in (2, 4, 6):
            d = (sub.taylor_sin(x + h, n) - sub.taylor_sin(x - h, n)) / (2 * h)
            assert abs(d - sub.taylor_cos(x, n)) < 1e-8
