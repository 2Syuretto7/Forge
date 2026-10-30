import math
import sub


def test_classic_limits():
    assert abs(sub.estimate_limit(lambda x: math.sin(x) / x, 0) - 1) < 1e-8
    assert abs(sub.estimate_limit(lambda x: (1 + x) ** (1 / x), 0) - math.e) < 1e-6
    assert abs(sub.estimate_limit(lambda x: (x * x - 1) / (x - 1), 1) - 2) < 1e-6


def test_no_limit():
    assert sub.estimate_limit(lambda x: 1.0 if x > 0 else 0.0, 0) is None
    assert sub.estimate_limit(lambda x: 1 / x, 0) is None


def test_tables_can_be_fooled():
    f = lambda x: math.sin(math.pi / x)  # noqa: E731
    vals = sub.approach(f, 0, 1, 8)
    assert all(abs(v) < 1e-6 for v in vals), "at x = 10^-k the samples all land near zeros of the sine"
    assert abs(f(1 / 1000.5)) > 0.99, "yet the function keeps oscillating between -1 and 1"
