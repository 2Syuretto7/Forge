import numpy as np
import sub


def test_grad_candidate_probability():
    for s in [0.2, 0.5, 0.8]:
        for b, r in [(20, 5), (16, 8)]:
            num = (sub.candidate_probability(s + 1e-6, b, r) - sub.candidate_probability(s - 1e-6, b, r)) / 2e-6
            assert abs(sub.dprob_ds(s, b, r) - num) < 1e-6


def test_s_curve():
    assert sub.candidate_probability(0.0, 20, 5) == 0 and sub.candidate_probability(1.0, 20, 5) == 1
    assert sub.candidate_probability(0.9, 20, 5) > 0.99 and sub.candidate_probability(0.3, 20, 5) < 0.05
    t = sub.threshold(20, 5)
    assert abs(sub.candidate_probability(t, 20, 5) - (1 - (1 - 1 / 20) ** 20)) < 1e-12


def test_choose_bands():
    b, r = sub.choose_bands(128, 0.8)
    assert b * r == 128 and abs(sub.threshold(b, r) - 0.8) < 0.1
    assert sub.choose_bands(128, 0.3)[1] < r
