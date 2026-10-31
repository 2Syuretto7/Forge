import numpy as np
import sub

rng = np.random.default_rng(3)
X = rng.normal(size=(20, 4))
params = (rng.normal(size=(6, 4)), rng.normal(size=6) * 0.1 + 0.3, rng.normal(size=(6, 4)), rng.normal(size=4) * 0.1)


def test_grad_sae():
    _, grads = sub.sae_loss(params, X, 0.05)
    for k in range(4):
        num = np.zeros_like(params[k])
        for idx in np.ndindex(params[k].shape):
            P = [p.copy() for p in params]
            P[k][idx] += 1e-6
            up = sub.sae_loss(tuple(P), X, 0.05)[0]
            P[k][idx] -= 2e-6
            num[idx] = (up - sub.sae_loss(tuple(P), X, 0.05)[0]) / 2e-6
        assert np.allclose(grads[k], num, atol=1e-6)
