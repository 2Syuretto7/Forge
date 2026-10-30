import math
from fractions import Fraction
import sub


def test_correct_versions_agree():
    assert sub.p_two_aces() == sub.p_two_aces_ordered() == Fraction(1, 221)


def test_mixed_is_wrong_by_k_factorial():
    assert sub.p_two_aces_mixed() == sub.mismatch_factor(2) * sub.p_two_aces()


def test_simulation_sides_with_the_correct_answer():
    est = sub.simulate(40000)
    p = 1 / 221
    se = math.sqrt(p * (1 - p) / 40000)
    assert abs(est - p) < 4 * se
    assert abs(est - 2 * p) > 4 * se
