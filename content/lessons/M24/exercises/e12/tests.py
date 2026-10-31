import numpy as np
import sub

A = 4.7534
P = sub.upper_tail(A)


def test_naive_is_hopeless():
    h = sub.naive_hits(A, 4 * 10**6, np.random.default_rng(50))
    assert 0 <= h <= 15


def test_importance_sampling_nails_it():
    est, se = sub.is_rare(A, sub.best_shift(A), 100000, np.random.default_rng(51))
    assert abs(est / P - 1) < 0.02 and se / P < 0.01, (est / P, se / P)


def test_chunks():
    assert sub.naive_hits(-50.0, 2500, np.random.default_rng(2), chunk=1000) == 2500
