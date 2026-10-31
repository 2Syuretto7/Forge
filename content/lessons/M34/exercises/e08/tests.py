import numpy as np
import sub


def test_above_and_below():
    rng = np.random.default_rng(0)
    n, p = 800, 200
    for ell in (0.2, 1.5, 3.0):
        tops, ovs = zip(*[sub.top_eig_and_overlap(sub.spiked_samples(n, p, ell, rng)) for _ in range(3)])
        assert abs(np.mean(tops) / sub.bbp_top(ell, 0.25) - 1) < 0.05, (ell, tops)
        assert abs(np.mean(ovs) - sub.bbp_overlap(ell, 0.25)) < 0.1, (ell, ovs)
    assert sub.bbp_top(0.5, 0.25) == 2.25 and sub.bbp_overlap(0.5, 0.25) == 0.0
