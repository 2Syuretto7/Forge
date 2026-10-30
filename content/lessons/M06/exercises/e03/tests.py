import math
import random
import sub


def test_series_near_zero():
    assert abs(sub.exp_series(1.0) - math.e) < 1e-14
    assert abs(sub.exp_series(-0.5) - math.exp(-0.5)) < 1e-15


def test_exp_everywhere():
    for x in [-700, -50, -3.7, 0, 0.001, 2.5, 20, 100, 700]:
        assert math.isclose(sub.exp(x), math.exp(x), rel_tol=1e-12), x


def test_invariant_exponent_rule():
    rnd = random.Random(0)
    for _ in range(500):
        a, b = rnd.uniform(-20, 20), rnd.uniform(-20, 20)
        assert math.isclose(sub.exp(a) * sub.exp(b), sub.exp(a + b), rel_tol=1e-12)
