import numpy as np
import sub


def test_low_rank_update():
    rng = np.random.default_rng(0)
    D = rng.standard_normal((40, 4)) @ rng.standard_normal((4, 30)) + 0.05 * rng.standard_normal((40, 30))
    assert sub.rank_r_error(D, 4) < 0.03 and sub.rank_r_error(D, 2) > 0.2
    assert sub.effective_rank(D) <= 4
    assert sub.effective_rank(rng.standard_normal((40, 30))) > 15
