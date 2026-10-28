import numpy as np
import sub

rng = np.random.default_rng(1)
logits = rng.normal(size=(7, 5))
targets = rng.integers(0, 5, 7)
mask = np.array([0, 0, 0, 1, 1, 1, 1], dtype=float)


def test_grad_masked_ce():
    loss, g = sub.masked_cross_entropy(logits, targets, mask)
    num = np.zeros_like(logits)
    for idx in np.ndindex(logits.shape):
        E = np.zeros_like(logits); E[idx] = 1e-6
        num[idx] = (sub.masked_cross_entropy(logits + E, targets, mask)[0] - sub.masked_cross_entropy(logits - E, targets, mask)[0]) / 2e-6
    assert np.allclose(g, num, atol=1e-8)
    assert np.all(g[:3] == 0)


def test_value():
    p = np.exp(logits) / np.exp(logits).sum(1, keepdims=True)
    expected = -np.log(p[np.arange(7), targets])[3:].mean()
    assert abs(sub.masked_cross_entropy(logits, targets, mask)[0] - expected) < 1e-12
