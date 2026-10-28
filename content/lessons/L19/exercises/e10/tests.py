import numpy as np
import sub


def test_ratios_and_flags():
    params = {"embed": np.ones((4, 4)), "attn": 2 * np.ones((2, 2)), "head": np.ones(3)}
    updates = {"embed": 1e-3 * np.ones((4, 4)), "attn": 0.1 * np.ones((2, 2)), "head": 1e-7 * np.ones(3)}
    r = sub.update_ratios(params, updates)
    assert abs(r["embed"] - 1e-3) < 1e-15 and abs(r["attn"] - 0.05) < 1e-15 and abs(r["head"] - 1e-7) < 1e-20
    assert sub.flag_layers(r) == ["attn", "head"]
