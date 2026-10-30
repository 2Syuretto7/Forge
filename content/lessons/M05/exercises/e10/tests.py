import sub


def test_fit_slope():
    assert abs(sub.fit_slope([1, 2, 3], [2, 4, 6]) - 2) < 1e-12


def test_single_loop_is_linear():
    p = sub.measured_exponent(sub.single_loop, [2000, 4000, 8000, 16000])
    assert 0.6 < p < 1.4, p


def test_double_loop_is_quadratic():
    p = sub.measured_exponent(sub.double_loop, [40, 80, 160])
    assert 1.5 < p < 2.5, p
