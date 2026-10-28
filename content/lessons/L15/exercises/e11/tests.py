import numpy as np
import sub

E, K, g = 1.69, 813.68, 0.15355


def frontier(C):
    return E + K * (C / 6) ** -g


def test_floor_fit_recovers_the_frontier():
    C = np.logspace(18, 21, 8)
    E_fit, k, gam = sub.fit_floor(C, frontier(C))
    assert abs(E_fit - E) < 0.02 and abs(gam - g) < 0.01


def test_narrow_range_pure_fit_is_optimistic():
    C = np.logspace(18, 21, 8)
    pure, floor = sub.extrapolation_errors(C, frontier(C), 1e24, frontier(1e24))
    assert pure < -0.1 and abs(floor) < 0.01


def test_wider_range_helps_the_pure_fit():
    narrow = sub.extrapolation_errors(np.logspace(18, 19, 8), frontier(np.logspace(18, 19, 8)), 1e24, frontier(1e24))[0]
    wide = sub.extrapolation_errors(np.logspace(18, 22, 8), frontier(np.logspace(18, 22, 8)), 1e24, frontier(1e24))[0]
    assert abs(wide) < abs(narrow)
