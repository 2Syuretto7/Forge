import numpy as np
import sub

rng = np.random.default_rng(3)


def _check(causal):
    Q, K, V = rng.normal(size=(5, 4)), rng.normal(size=(5, 4)), rng.normal(size=(5, 3))
    G = rng.normal(size=(5, 3))
    O, P = sub.attention(Q, K, V, causal=causal)
    grads = sub.attention_backward(G, Q, K, V, P)
    f = lambda Q, K, V: float(np.sum(sub.attention(Q, K, V, causal=causal)[0] * G))
    for pos, (arr, g) in enumerate(zip((Q, K, V), grads)):
        num = np.zeros_like(arr)
        for idx in np.ndindex(arr.shape):
            args = [Q.copy(), K.copy(), V.copy()]
            args[pos][idx] += 1e-6
            fp = f(*args)
            args[pos][idx] -= 2e-6
            num[idx] = (fp - f(*args)) / 2e-6
        assert np.allclose(g, num, atol=1e-7), (causal, pos)


def test_grad_causal():
    _check(True)


def test_grad_full():
    _check(False)
