import sub


def test_small_cases_agree():
    assert abs(sub.comb_float_factorials(52, 5) - 2598960) < 1e-6


def test_factorial_route_overflows():
    assert sub.largest_float_factorial() == 170
    try:
        sub.comb_float_factorials(200, 100)
    except OverflowError:
        return
    raise AssertionError("float(200!) should overflow")


def test_log_route_works():
    exact = sub.comb_exact(200, 100)
    assert abs(sub.comb_logs(200, 100) / exact - 1) < 1e-10
