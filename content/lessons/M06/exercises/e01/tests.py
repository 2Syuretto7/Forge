import math
import random
import sub


def test_values():
    assert sub.power_int(2, 10) == 1024
    assert sub.power_int(2, -3) == 0.125
    assert sub.power_int(7, 0) == 1
    assert abs(sub.nth_root(8, 3) - 2) < 1e-12
    assert abs(sub.power_rational(8, 2, 3) - 4) < 1e-12
    assert abs(sub.nth_root(0.25, 2) - 0.5) < 1e-12


def test_invariant_power_rules():
    rnd = random.Random(0)
    for _ in range(500):
        a = rnd.uniform(0.5, 2)
        m, n = rnd.randint(-8, 8), rnd.randint(-8, 8)
        assert math.isclose(sub.power_int(a, m) * sub.power_int(a, n), sub.power_int(a, m + n), rel_tol=1e-12)
        q = rnd.randint(1, 7)
        assert math.isclose(sub.power_int(sub.nth_root(a, q), q), a, rel_tol=1e-12)
