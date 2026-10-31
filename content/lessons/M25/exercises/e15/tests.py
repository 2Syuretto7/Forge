import math
import numpy as np
import sub


def test_block_bootstrap_fixes_the_error_bar():
    rng = np.random.default_rng(0)
    x = sub.ar1(2000, 0.8, rng)
    true = math.sqrt(1.8 / 0.2 / 2000)
    iid = sub.iid_bootstrap_se(x, 1000, rng)
    blk = sub.block_bootstrap_se(x, 50, 1000, rng)
    assert iid / true < 0.45, iid / true
    assert 0.7 < blk / true < 1.3, blk / true


def test_independent_data_agree():
    rng = np.random.default_rng(1)
    x = rng.standard_normal(2000)
    iid = sub.iid_bootstrap_se(x, 1000, rng)
    blk = sub.block_bootstrap_se(x, 20, 1000, rng)
    assert abs(iid / blk - 1) < 0.15 and abs(iid * math.sqrt(2000) - 1) < 0.1
