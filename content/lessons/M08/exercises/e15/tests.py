from fractions import Fraction
import sub


def test_values():
    assert sub.p_six_in_rolls(4) == Fraction(671, 1296)
    assert sub.p_by_adding(4) == Fraction(2, 3)
    assert sub.first_impossible() == 7


def test_overcount():
    assert sub.overcount(1) == 0
    assert all(sub.overcount(n) > 0 for n in range(2, 20))


def test_de_mere():
    assert float(sub.p_six_in_rolls(4)) > 0.5
    assert float(sub.p_double_six(24)) < 0.5 < float(sub.p_double_six(25))
