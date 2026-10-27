import numpy as np
import sub


def test_theory_values():
    assert abs(sub.variance_theory(20, 10) - 10 / 9) < 1e-12
    assert abs(sub.variance_theory(20, 60) - 20 / 39) < 1e-12
    assert sub.variance_theory(20, 20) == float("inf")


def test_simulation_matches_theory_below_threshold():
    s = sub.variance_sim(20, 10, trials=3000, seed=1)
    assert abs(s / sub.variance_theory(20, 10) - 1) < 0.1, s


def test_simulation_matches_theory_above_threshold():
    s = sub.variance_sim(20, 40, trials=3000, seed=2)
    assert abs(s / sub.variance_theory(20, 40) - 1) < 0.1, s
