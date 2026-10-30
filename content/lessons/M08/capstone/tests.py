import math
from fractions import Fraction
import sub


def test_exact_values():
    E = sub.EXACT
    assert E["sum_seven"] == Fraction(1, 6)
    assert E["two_aces"] == Fraction(1, 221)
    assert E["full_house"] == Fraction(3744, 2598960)
    assert E["three_heads"] == Fraction(520, 1024)
    assert E["committee"] == Fraction(3, 10)
    assert E["same_suit_3"] == Fraction(4 * 286, 22100)
    assert abs(float(E["birthday_23"]) - 0.5072972343239854) < 1e-12
    assert abs(float(E["derangement_10"]) - 1 / math.e) < 1e-7
    assert abs(float(E["double_six_24"]) - 0.4914038761309034) < 1e-12
    assert set(E) == set(sub.PUZZLES) == set(sub.TRIALS)


def test_simulations_agree_within_three_standard_errors():
    rows = sub.report(4000)
    assert [r["name"] for r in rows] == list(sub.PUZZLES)
    for r in rows:
        assert abs(r["z"]) <= 3, f"{r['name']}: exact {r['exact']:.4f}, simulated {r['estimate']:.4f}, z = {r['z']:.2f}"


def test_hash_plan():
    plan = sub.hash_plan(10 ** 7, 1e-9)
    pairs = math.comb(10 ** 7, 2)
    assert pairs / 2 ** plan["bits"] <= 1e-9 < pairs / 2 ** (plan["bits"] - 1)
    assert abs(plan["expected_pairs_64"] - pairs / 2 ** 64) < 1e-15
