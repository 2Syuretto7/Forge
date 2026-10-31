import numpy as np
import sub


def test_scale():
    assert abs(sub.branch_scale_for(25) - 0.2) < 1e-12


def test_scaling_makes_res_trainable():
    r = sub.compare_branch_scaling()
    assert r["unscaled"] > 1.0, r
    assert r["scaled"] < 0.4, r
