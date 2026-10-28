import numpy as np
import sub

rng = np.random.default_rng(5)
G = np.exp(rng.normal(-16, 2, size=10000)).astype(np.float32)


def test_underflow():
    assert sub.underflow_fraction(G) > 0.15
    assert sub.underflow_fraction(G, 2 ** 16) < 0.001


def test_grad_scaled_loss():
    X, y, w = rng.normal(size=(20, 3)), rng.normal(size=20), rng.normal(size=3)
    S = 1024.0
    L, g = sub.scaled_loss_and_grad(w, X, y, S)
    num = np.array([(sub.scaled_loss_and_grad(w + e, X, y, S)[0] - sub.scaled_loss_and_grad(w - e, X, y, S)[0]) / 2e-6 for e in np.eye(3) * 1e-6])
    assert np.allclose(g, num, rtol=1e-6)
    _, g1 = sub.scaled_loss_and_grad(w, X, y, 1.0)
    assert np.allclose(g / S, g1)
