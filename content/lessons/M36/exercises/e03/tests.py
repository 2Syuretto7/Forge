import numpy as np
import sub


def test_baselines():
    rng = np.random.default_rng(0)
    z = np.array([0.3, -0.2, 0.8, 0.0])
    r = np.array([1.0, 0.0, 2.0, 0.5])
    p = np.exp(z) / np.exp(z).sum()
    exact = p * (r - p @ r)
    shifted = r + 10
    v0 = sub.total_variance(sub.estimates(z, r, 50000, rng, b=p @ r))
    v_shift = sub.total_variance(sub.estimates(z, shifted, 50000, rng))
    v_shift_b = sub.total_variance(sub.estimates(z, shifted, 50000, rng, b=p @ shifted))
    assert v_shift > 40 * v0 and abs(v_shift_b / v0 - 1) < 0.05
    for b in (0.0, 5.0, sub.optimal_baseline(z, shifted)):
        G = sub.estimates(z, shifted, 200000, rng, b=b)
        assert np.max(np.abs(G.mean(axis=0) - exact)) < 0.05
    vb = sub.total_variance(sub.estimates(z, r, 50000, rng, b=sub.optimal_baseline(z, r)))
    assert vb <= v0 * 1.02
