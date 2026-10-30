import math
import sub

GPU_HOURS = [
    (1e8, 1e8, "*"),
    (2e9, 2e9, "*"),
    (3, 10, "*"),
    (3e13, 3e14, "/"),
    (3600, 3600, "/"),
]


def test_fermi_interval():
    lo, hi = sub.fermi(GPU_HOURS)
    assert math.isclose(lo, 6e17 / 3e14 / 3600, rel_tol=1e-12)
    assert math.isclose(hi, 2e18 / 3e13 / 3600, rel_tol=1e-12)


def test_central_brackets_the_computed_value():
    c = sub.central(GPU_HOURS)
    truth = 6 * 1e8 * 2e9 / 1e14 / 3600
    assert max(c / truth, truth / c) < sub.worst_factor(GPU_HOURS)


def test_typical_is_smaller_than_worst():
    nine = [(1, 4, "*")] * 9  # each within a factor of 2 of its midpoint 2
    assert math.isclose(sub.worst_factor(nine), 2 ** 9, rel_tol=1e-9)
    assert math.isclose(sub.typical_factor(nine), 2 ** 3, rel_tol=1e-9)
    one = [(1, 9, "*"), (5, 5, "/")]
    assert math.isclose(sub.typical_factor(one), sub.worst_factor(one), rel_tol=1e-12)


def test_division_flips_the_ends():
    lo, hi = sub.fermi([(10, 20, "*"), (2, 5, "/")])
    assert (lo, hi) == (2.0, 10.0)
