import numpy as np
import sub

P = np.random.default_rng(2).normal(size=(500, 2))


def test_agree_closely():
    assert sub.gap(P, 1, 0.01) < 1e-14
    assert sub.gap(P, 5000, 0.001) < 1e-10


def test_gap_grows():
    g = sub.gap_growth(P, [10, 100, 1000, 10000], 0.0003)
    assert g[3] > g[1] and g[2] > g[0]
    assert g[3] < 1e-9
