import math
import sub


def test_compounding():
    assert sub.e_compounding(1) == 2
    assert abs(sub.e_compounding(12) - 2.613035290224676) < 1e-12
    assert abs(sub.e_compounding(10 ** 6) - math.e) < 2e-6


def test_series():
    assert abs(sub.e_series(15) - math.e) < 1e-11
    assert sub.terms_for_digits(12) <= 16
    assert sub.e_series(1) == 1


def test_compounding_error_law():
    for n in [100, 1000, 10000]:
        assert abs(sub.compounding_error(n) / (math.e / (2 * n)) - 1) < 0.01
