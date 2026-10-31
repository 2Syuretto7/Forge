import numpy as np
import sub


def test_minimum_at_p_equals_n():
    ps = list(range(20, 61, 4))
    curve = sub.sigma_min_curve(40, ps, trials=10, seed=0)
    assert ps[int(np.argmin(curve))] == 40
    assert curve[ps.index(40)] < 0.3 * curve[0] and curve[ps.index(40)] < 0.3 * curve[-1]


def test_marchenko_pastur_edge():
    for p in [100, 400]:
        s = np.mean([sub.sigma_min(200, p, seed) for seed in range(3)])
        assert abs(s / sub.mp_edge(200, p) - 1) < 0.15, (p, s)
