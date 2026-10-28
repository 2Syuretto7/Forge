import numpy as np
import sub

rng = np.random.default_rng(0)
L = rng.normal(size=(4, 6)) * 3 + 5
y = np.array([0, 2, 5, 1])


def test_grad_z_loss():
    _, g = sub.ce_with_z_loss(L, y, 1e-2)
    num = np.zeros_like(L)
    for idx in np.ndindex(L.shape):
        P = L.copy()
        P[idx] += 1e-6
        up = sub.ce_with_z_loss(P, y, 1e-2)[0]
        P[idx] -= 2e-6
        num[idx] = (up - sub.ce_with_z_loss(P, y, 1e-2)[0]) / 2e-6
    assert np.allclose(g, num, atol=1e-8)


def test_values():
    lse = np.log(np.exp(L).sum(1))
    ce = np.mean(lse - L[np.arange(4), y])
    assert abs(sub.ce_with_z_loss(L, y, 0)[0] - ce) < 1e-12
    assert abs(sub.ce_with_z_loss(L, y, 0.1)[0] - ce - 0.1 * np.mean(lse ** 2)) < 1e-12
    assert np.isfinite(sub.ce_with_z_loss(L * 200, y, 1e-4)[0])
