import numpy as np
import sub

rng = np.random.default_rng(4)
n, d, h = 6, 8, 2
X = rng.normal(size=(n, d))
W = [rng.normal(size=(d, d)) * 0.3 for _ in range(4)]


def test_split_merge():
    Y = sub.split_heads(X, 4)
    assert Y.shape == (4, 6, 2) and np.allclose(Y[1], X[:, 2:4])
    assert np.allclose(sub.merge_heads(Y), X)


def test_against_per_head_loop():
    Y, cache = sub.mha_forward(X, *W, h)
    outs = []
    for i in range(h):
        cols = slice(i * d // h, (i + 1) * d // h)
        O, _ = sub.attention((X @ W[0])[:, cols], (X @ W[1])[:, cols], (X @ W[2])[:, cols])
        outs.append(O)
    assert np.allclose(Y, np.hstack(outs) @ W[3])
    assert cache[4].shape == (h, n, n)


def test_one_head():
    Y, _ = sub.mha_forward(X, *W, 1)
    O, _ = sub.attention(X @ W[0], X @ W[1], X @ W[2])
    assert np.allclose(Y, O @ W[3])
