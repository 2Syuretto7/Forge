import numpy as np
import sub


def test_methods_agree_on_small_data():
    v = np.random.default_rng(1).integers(0, 5, size=400).astype(float)
    a = sub.bootstrap_by_index(v, 4000, np.random.default_rng(2))
    b = sub.bootstrap_by_counts(v, 4000, np.random.default_rng(3))
    assert abs(a.mean() - b.mean()) < 0.01 and abs(a.std() / b.std() - 1) < 0.06


def test_full_size():
    rng = np.random.default_rng(4)
    correct = (rng.random(100000) < 0.83).astype(float)
    m = sub.bootstrap_by_counts(correct, 2000, rng)
    assert m.shape == (2000,)
    se = np.sqrt(correct.mean() * (1 - correct.mean()) / 100000)
    assert abs(m.std() / se - 1) < 0.06


def test_pairing():
    rng = np.random.default_rng(5)
    hard = rng.random(100000)
    a = (hard < 0.80).astype(float)
    b = ((hard < 0.80) | (rng.random(100000) < 0.03)).astype(float)
    b[rng.random(100000) < 0.01] = 0.0
    lo, hi = sub.paired_interval(a, b, 2000, rng)
    unpaired = 2 * 1.96 * np.sqrt(a.var() / 1e5 + b.var() / 1e5)
    assert lo < b.mean() - a.mean() < hi
    assert (hi - lo) < unpaired / 2, (hi - lo, unpaired)
