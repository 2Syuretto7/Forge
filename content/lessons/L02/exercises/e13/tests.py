import math
import numpy as np
import sub


def test_logpdf_integrates_to_one():
    t = (np.arange(10000) + 0.5) / 10000
    for a, b in [(4, 2), (7, 5), (1, 1)]:
        assert abs(np.sum(np.exp(sub.beta_logpdf(t, a, b))) / 10000 - 1) < 1e-4
    assert abs(sub.beta_logpdf(np.array([0.5]), 2, 2)[0] - math.log(1.5)) < 1e-12


def test_puzzle_answer():
    p = sub.prob_a_better_grid(3, 4, 6, 10)
    assert abs(p - 0.65385) < 1e-3, f"got {p:.5f}"


def test_monte_carlo_agrees_with_integration():
    g = sub.prob_a_better_grid(3, 4, 6, 10)
    mc = sub.prob_a_better_mc(3, 4, 6, 10, draws=200000, seed=3)
    assert abs(mc - g) < 0.006


def test_symmetry_and_equal_data():
    p = sub.prob_a_better_grid(2, 5, 7, 9)
    q = sub.prob_a_better_grid(7, 9, 2, 5)
    assert abs(p + q - 1) < 1e-3
    assert abs(sub.prob_a_better_grid(5, 10, 5, 10) - 0.5) < 1e-3
