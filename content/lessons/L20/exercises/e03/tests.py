import numpy as np
import sub

rng = np.random.default_rng(1)
x = rng.normal(size=(4, 6))
W0 = rng.normal(size=(5, 6))
A = rng.normal(size=(2, 6))
B = rng.normal(size=(5, 2))
dy = rng.normal(size=(4, 5))


def loss(A_, B_, x_):
    return np.sum(sub.lora_forward(x_, W0, A_, B_, 4.0) * dy)


def test_zero_b_is_the_base_model():
    assert np.allclose(sub.lora_forward(x, W0, A, np.zeros((5, 2)), 4.0), x @ W0.T)


def test_grad_lora():
    dA, dB, dx = sub.lora_backward(dy, x, W0, A, B, 4.0)
    for M, G, which in [(A, dA, 0), (B, dB, 1), (x, dx, 2)]:
        num = np.zeros_like(M)
        for idx in np.ndindex(M.shape):
            P = M.copy()
            P[idx] += 1e-6
            args = [A, B, x]
            args[which] = P
            up = loss(*args)
            P[idx] -= 2e-6
            num[idx] = (up - loss(*args)) / 2e-6
        assert np.allclose(G, num, atol=1e-6)
