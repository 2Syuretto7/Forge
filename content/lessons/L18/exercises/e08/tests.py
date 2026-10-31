import numpy as np
import sub

rng = np.random.default_rng(3)
W = rng.normal(size=(5, 16))
X = rng.normal(size=(40, 16))


def test_grad_output_error():
    Wh = W + 0.1 * rng.normal(size=W.shape)
    _, g = sub.output_error(Wh, W, X)
    num = np.zeros_like(W)
    for idx in np.ndindex(W.shape):
        P = Wh.copy()
        P[idx] += 1e-6
        up = sub.output_error(P, W, X)[0]
        P[idx] -= 2e-6
        num[idx] = (up - sub.output_error(P, W, X)[0]) / 2e-6
    assert np.allclose(g, num, atol=1e-6)


def test_groups():
    errs = [sub.output_error(sub.group_quantize(W, 4, g), W, X)[0] for g in [16, 8, 4]]
    assert errs[0] > errs[1] > errs[2]
    assert sub.output_error(sub.group_quantize(W, 8, 16), W, X)[0] < errs[2]
