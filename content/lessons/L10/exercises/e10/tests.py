import numpy as np
import sub

rng = np.random.default_rng(10)
Z = rng.normal(size=(5, 6)) * 2
Y = rng.integers(0, 6, size=5)


def test_reduces_to_cross_entropy():
    loss, _ = sub.smoothed_xent(Z, Y, 0.0)
    p = np.exp(Z - Z.max(axis=1, keepdims=True))
    p /= p.sum(axis=1, keepdims=True)
    assert np.isclose(loss, -np.mean(np.log(p[np.arange(5), Y])))


def test_grad_smoothed():
    _, g = sub.smoothed_xent(Z, Y, 0.1)
    num = np.zeros_like(Z)
    for idx in np.ndindex(Z.shape):
        E = np.zeros_like(Z)
        E[idx] = 1e-6
        num[idx] = (sub.smoothed_xent(Z + E, Y, 0.1)[0] - sub.smoothed_xent(Z - E, Y, 0.1)[0]) / 2e-6
    assert np.allclose(g, num, atol=1e-8)
