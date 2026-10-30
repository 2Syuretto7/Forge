import math
import random
import sub


def test_ln():
    for y in [1e-300, 0.5, 1.0, math.e, 10, 1e300]:
        assert abs(sub.ln(y) - math.log(y)) < 1e-11 * max(1, abs(math.log(y))), y
    try:
        sub.ln(0)
    except ValueError:
        pass
    else:
        raise AssertionError("ln(0) should raise ValueError")


def test_bases_and_digits():
    assert abs(sub.log_base(1024, 2) - 10) < 1e-12
    assert abs(sub.log_base(1000, 10) - 3) < 1e-12
    assert [sub.digits(n) for n in [1, 9, 10, 99, 100, 999, 1000, 10 ** 15, 10 ** 15 - 1]] == [1, 1, 2, 2, 3, 3, 4, 16, 15]


def test_invariant_product_rule():
    rnd = random.Random(0)
    for _ in range(300):
        x, y = math.exp(rnd.uniform(-50, 50)), math.exp(rnd.uniform(-50, 50))
        assert abs(sub.ln(x * y) - (sub.ln(x) + sub.ln(y))) < 1e-10
