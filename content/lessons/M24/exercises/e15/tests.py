import numpy as np
import sub

CH = sub.ar1_chains(200, 5000, 0.9, np.random.default_rng(80))


def test_inflation():
    assert abs(sub.inflation(0.9) - 19**0.5) < 1e-12 and sub.inflation(0.0) == 1.0
    ratios = [sub.batch_means_se(c) / sub.naive_se(c) for c in CH[:40]]
    assert 0.75 * sub.inflation(0.9) < np.mean(ratios) < 1.15 * sub.inflation(0.9), np.mean(ratios)


def test_coverage():
    naive = np.mean([abs(c.mean()) <= 1.96 * sub.naive_se(c) for c in CH])
    batch = np.mean([abs(c.mean()) <= 2.01 * sub.batch_means_se(c) for c in CH])
    assert naive < 0.6, naive
    assert batch > 0.85, batch
