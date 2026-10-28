import numpy as np
import sub

rng = np.random.default_rng(1)
hard = rng.random(500) < 0.4
a = (~hard | (rng.random(500) < 0.15)).astype(float)
b = a.copy()
flip = rng.choice(np.flatnonzero(a == 1), 25, replace=False)
b[flip] = 0


def test_paired_is_sharper():
    d, lo, hi = sub.paired_bootstrap(a, b)
    assert abs(d - 0.05) < 1e-12 and lo > 0
    n = len(a)
    unpaired_halfwidth = 1.96 * np.sqrt(a.mean() * (1 - a.mean()) / n + b.mean() * (1 - b.mean()) / n)
    assert (hi - lo) / 2 < 0.6 * unpaired_halfwidth
