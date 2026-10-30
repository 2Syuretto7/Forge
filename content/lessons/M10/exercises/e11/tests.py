import sub


def test_fit_exponent_exact():
    ns = [100, 200, 400, 800]
    assert abs(sub.fit_exponent(ns, [3e-9 * n ** 3 for n in ns]) - 3) < 1e-9
    assert abs(sub.fit_exponent(ns, [5 * n ** 2 for n in ns]) - 2) < 1e-9


def test_predicted():
    assert sub.predicted_ratio(256, 512) == 8


def test_measured_growth():
    small, large = sub.time_matmul(64), sub.time_matmul(256)
    assert large > small
