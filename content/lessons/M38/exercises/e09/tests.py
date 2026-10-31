import numpy as np
import sub


def test_rank_tradeoff():
    rng = np.random.default_rng(0)
    n, k, d = 1500, 32, 24
    X = rng.standard_normal((n, k))
    W0 = rng.standard_normal((k, d)) / np.sqrt(k)
    dW = rng.standard_normal((k, 4)) @ rng.standard_normal((4, d)) / np.sqrt(k) + 0.002 * rng.standard_normal((k, d))
    Y = X @ (W0 + dW) + 0.1 * rng.standard_normal((n, d))
    sweep = sub.rank_sweep(X, Y, W0, [1, 2, 4, 8])
    full = sub.full_loss(X, Y)
    assert sub.smallest_rank_within(sweep, full) == 4
    assert sweep[4][1] < 1 / 3 and sweep[2][0] > 1.5 * full
