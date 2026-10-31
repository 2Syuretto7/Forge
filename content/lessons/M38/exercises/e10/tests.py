import numpy as np
import sub


def test_full_rank_update_defeats_lora():
    rng = np.random.default_rng(0)
    n, k, d = 2000, 24, 16
    X = rng.standard_normal((n, k))
    W0 = rng.standard_normal((k, d)) / np.sqrt(k)
    dW = rng.standard_normal((k, d)) / np.sqrt(k)
    Y = X @ (W0 + dW) + 0.1 * rng.standard_normal((n, d))
    full = sub.predicted_floor(X, dW, d, 0.01)
    l4 = sub.train_loss(X, Y, W0, 4)
    assert l4 > 3 * full
    for r in (4, 8):
        assert abs(sub.train_loss(X, Y, W0, r) / sub.predicted_floor(X, dW, r, 0.01) - 1) < 0.1
