import numpy as np
import sub


def test_grad_dpo_loss():
    rng = np.random.default_rng(0)
    K = 5
    z, ref = rng.standard_normal(K), sub.log_softmax(rng.standard_normal(K))
    N = rng.integers(0, 6, (K, K)).astype(float)
    np.fill_diagonal(N, 0)
    g = sub.grad_dpo_loss(z, ref, N, 0.7)
    h = 1e-6
    for k in range(K):
        e = np.zeros(K)
        e[k] = h
        num = (sub.dpo_loss(z + e, ref, N, 0.7) - sub.dpo_loss(z - e, ref, N, 0.7)) / (2 * h)
        assert abs(num - g[k]) < 1e-7
    assert abs(g.sum()) < 1e-12
