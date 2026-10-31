import numpy as np
import sub

rng = np.random.default_rng(0)
x, W = rng.normal(size=(5, 6)), rng.normal(size=(4, 6))
A, B = rng.normal(size=(2, 6)), rng.normal(size=(4, 2))
gy = rng.normal(size=(5, 4))


def test_grad_lora():
    dA, dB = sub.lora_backward(x, A, B, 8.0, gy)
    f = lambda A_, B_: (gy * sub.lora_forward(x, W, A_, B_, 8.0)).sum()
    numA = np.zeros_like(A)
    for idx in np.ndindex(A.shape):
        E = np.zeros_like(A); E[idx] = 1e-6
        numA[idx] = (f(A + E, B) - f(A - E, B)) / 2e-6
    numB = np.zeros_like(B)
    for idx in np.ndindex(B.shape):
        E = np.zeros_like(B); E[idx] = 1e-6
        numB[idx] = (f(A, B + E) - f(A, B - E)) / 2e-6
    assert np.allclose(dA, numA, atol=1e-6) and np.allclose(dB, numB, atol=1e-6)


def test_merge():
    assert np.allclose(x @ sub.merge(W, A, B, 8.0).T, sub.lora_forward(x, W, A, B, 8.0))
