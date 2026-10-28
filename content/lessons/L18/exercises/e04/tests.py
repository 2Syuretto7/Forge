import numpy as np
import sub

rng = np.random.default_rng(1)
X = rng.normal(size=(30, 4))
y = rng.normal(size=30)
w = rng.normal(size=4)


def test_grad_local_loss():
    _, g = sub.local_loss_grad(w, X, y)
    num = [(sub.local_loss_grad(w + e, X, y)[0] - sub.local_loss_grad(w - e, X, y)[0]) / 2e-6 for e in np.eye(4) * 1e-6]
    assert np.allclose(g, num, atol=1e-8)


def test_matches_full_batch():
    full = w - 0.1 * sub.local_loss_grad(w, X, y)[1]
    shards = [(X[:7], y[:7]), (X[7:20], y[7:20]), (X[20:], y[20:])]
    assert np.allclose(sub.dp_step(w, shards, 0.1), full)
    assert np.allclose(sub.dp_step(w, [(X, y)], 0.1), full)
