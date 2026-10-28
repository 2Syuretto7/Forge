import numpy as np
import sub

rng = np.random.default_rng(0)
logits = rng.normal(size=(6, 5)) * 2
targets = np.array([1, 4, 0, 2, 2, 3])
mask = np.array([0, 0, 1, 1, 0, 1], dtype=float)


def test_value():
    loss, g = sub.masked_ce(logits, targets, mask)
    logp = logits - np.log(np.exp(logits).sum(1, keepdims=True))
    assert abs(loss - (-logp[[2, 3, 5], targets[[2, 3, 5]]].mean())) < 1e-12
    assert np.all(g[[0, 1, 4]] == 0)


def test_grad_masked_ce():
    _, g = sub.masked_ce(logits, targets, mask)
    num = np.zeros_like(logits)
    for idx in np.ndindex(logits.shape):
        P = logits.copy()
        P[idx] += 1e-6
        up = sub.masked_ce(P, targets, mask)[0]
        P[idx] -= 2e-6
        num[idx] = (up - sub.masked_ce(P, targets, mask)[0]) / 2e-6
    assert np.allclose(g, num, atol=1e-8)
