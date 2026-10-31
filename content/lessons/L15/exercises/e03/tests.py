import numpy as np
import sub

rng = np.random.default_rng(3)


def test_layer_norm():
    x = rng.normal(size=(3, 8)) * 4 + 2
    y, _ = sub.layer_norm(x)
    assert np.allclose(y.mean(1), 0) and np.allclose(y.var(1), 1, atol=1e-4)


def test_grad_layer_norm():
    x = rng.normal(size=(2, 5))
    dy = rng.normal(size=(2, 5))
    _, cache = sub.layer_norm(x)
    dx = sub.layer_norm_backward(dy, cache)
    num = np.zeros_like(x)
    for idx in np.ndindex(x.shape):
        P = x.copy()
        P[idx] += 1e-6
        up = np.sum(sub.layer_norm(P)[0] * dy)
        P[idx] -= 2e-6
        num[idx] = (up - np.sum(sub.layer_norm(P)[0] * dy)) / 2e-6
    assert np.allclose(dx, num, atol=1e-7)


def test_qk_norm_bounds_logits():
    q = rng.normal(size=(6, 16)) * 50
    k = rng.normal(size=(6, 16)) * 50
    assert sub.max_attention_logit(q, k, False) > 100
    assert sub.max_attention_logit(q, k, True) <= np.sqrt(16) + 1e-6
