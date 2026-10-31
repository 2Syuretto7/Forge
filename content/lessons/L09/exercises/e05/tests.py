import numpy as np
import sub

rng = np.random.default_rng(5)
n, d, h = 5, 6, 3
X = rng.normal(size=(n, d))
W = [rng.normal(size=(d, d)) * 0.4 for _ in range(4)]
G = rng.normal(size=(n, d))


def test_grad_all_inputs():
    _, cache = sub.mha_forward(X, *W, h)
    grads = sub.mha_backward(G, cache, *W)
    params = [X] + W
    f = lambda ps: float(np.sum(sub.mha_forward(ps[0], *ps[1:], h)[0] * G))
    for pos, g in enumerate(grads):
        num = np.zeros_like(params[pos])
        for idx in np.ndindex(params[pos].shape):
            ps = [p.copy() for p in params]
            ps[pos][idx] += 1e-6
            fp = f(ps)
            ps[pos][idx] -= 2e-6
            num[idx] = (fp - f(ps)) / 2e-6
        assert np.allclose(g, num, atol=1e-7), pos
