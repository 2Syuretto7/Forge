import random
from fractions import Fraction

import sub


def test_partial_sums():
    s = sub.partial_sums(lambda k: Fraction(1, 2 ** k), 4)
    assert s == [Fraction(1, 2), Fraction(3, 4), Fraction(7, 8), Fraction(15, 16)]
    assert sub.partial_sums(lambda k: k, 4) == [1, 3, 6, 10]


def test_examples():
    assert sub.geometric_sum(Fraction(1, 2), 10) == Fraction(1023, 512)
    assert sub.geometric_closed(Fraction(1, 2), 10) == Fraction(1023, 512)
    assert sub.geometric_closed(Fraction(1), 7) == 7


def test_invariant_closed_form_is_exact():
    rnd = random.Random(0)
    for _ in range(300):
        r = Fraction(rnd.randint(-9, 9), rnd.randint(1, 9))
        n = rnd.randint(0, 25)
        assert sub.geometric_sum(r, n) == sub.geometric_closed(r, n), (r, n)
