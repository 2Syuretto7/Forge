import math
import random
import sub


def test_known_values():
    m, e = sub.to_scientific(299792458)
    assert e == 8 and abs(m - 2.99792458) < 1e-12
    m, e = sub.to_scientific(-0.00042)
    assert e == -4 and abs(m + 4.2) < 1e-12
    assert sub.to_scientific(0) == (0.0, 0)
    assert isinstance(sub.to_scientific(5e7)[1], int), "the exponent must be an int"


def test_exact_powers_and_rounding_edges():
    for k in range(-30, 31):
        m, e = sub.to_scientific(10.0 ** k)
        assert e == k and abs(m - 1) < 1e-12, (k, m, e)
    m, e = sub.to_scientific(1e23)
    assert 1 <= abs(m) < 10


def test_invariant_round_trip():
    rnd = random.Random(1)
    for _ in range(3000):
        x = rnd.choice([-1, 1]) * rnd.uniform(1, 10) * 10 ** rnd.randint(-40, 40)
        m, e = sub.to_scientific(x)
        assert 1 <= abs(m) < 10, (x, m, e)
        assert math.isclose(sub.from_scientific(m, e), x, rel_tol=1e-12), x


def test_format():
    assert sub.format_scientific(299792458, 3) == "3.00 x 10^8"
    assert sub.format_scientific(9996, 3) == "1.00 x 10^4"
    assert sub.format_scientific(0.000123456, 2) == "1.2 x 10^-4"
