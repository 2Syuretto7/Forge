import numpy as np
import sub

rng = np.random.default_rng(2)
W = rng.normal(size=(6, 10))
W[2] = 0


def test_roundtrip():
    q, s = sub.quantize_int8(W)
    assert q.dtype == np.int8 and np.abs(q).max() <= 127
    assert np.all(np.abs(sub.dequantize(q, s) - W) <= s[:, None] / 2 + 1e-12)


def test_matmul():
    x = rng.normal(size=(3, 10))
    q, s = sub.quantize_int8(W)
    assert np.allclose(sub.int8_matmul(x, q, s), x @ sub.dequantize(q, s).T)
    assert np.abs(sub.int8_matmul(x, q, s) - x @ W.T).max() < 0.05
