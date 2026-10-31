import numpy as np
import sub

rng = np.random.default_rng(10)
Z = rng.normal(size=(5, 23)) * 3
Y = rng.integers(0, 23, size=5)


def _ref(Z):
    m = Z.max(axis=1, keepdims=True)
    lse = (m + np.log(np.exp(Z - m).sum(axis=1, keepdims=True)))[:, 0]
    return float(np.mean(lse - Z[np.arange(5), Y]))


def test_loss():
    loss, _ = sub.fused_cross_entropy(Z, Y)
    assert abs(loss - _ref(Z)) < 1e-12
    big, _ = sub.fused_cross_entropy(Z * 100, Y)
    assert np.isfinite(big) and abs(big - _ref(Z * 100)) < 1e-9


def test_grad_fused_cross_entropy():
    _, d = sub.fused_cross_entropy(Z, Y)
    num = np.zeros_like(Z)
    for idx in np.ndindex(Z.shape):
        E = np.zeros_like(Z)
        E[idx] = 1e-6
        num[idx] = (_ref(Z + E) - _ref(Z - E)) / 2e-6
    assert np.allclose(d, num, atol=1e-8)
