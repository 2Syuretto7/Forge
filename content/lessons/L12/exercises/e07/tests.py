import numpy as np
import sub

rng = np.random.default_rng(7)
Q, K, V = rng.normal(size=(6, 4)), rng.normal(size=(6, 4)), rng.normal(size=(6, 3))
G = rng.normal(size=(6, 3))


def test_grad_flash_backward():
    O, L = sub.flash_attention(Q, K, V)
    grads = sub.flash_backward(G, Q, K, V, O, L, Bc=4)
    f = lambda Q, K, V: float(np.sum(sub.reference_attention(Q, K, V) * G))
    for pos, g in enumerate(grads):
        arr = (Q, K, V)[pos]
        num = np.zeros_like(arr)
        for idx in np.ndindex(arr.shape):
            args = [Q.copy(), K.copy(), V.copy()]
            args[pos][idx] += 1e-6
            fp = f(*args)
            args[pos][idx] -= 2e-6
            num[idx] = (fp - f(*args)) / 2e-6
        assert np.allclose(g, num, atol=1e-7), pos


def test_block_size_independent():
    O, L = sub.flash_attention(Q, K, V)
    a = sub.flash_backward(G, Q, K, V, O, L, Bc=1)
    b = sub.flash_backward(G, Q, K, V, O, L, Bc=6)
    assert all(np.allclose(x, y) for x, y in zip(a, b))
