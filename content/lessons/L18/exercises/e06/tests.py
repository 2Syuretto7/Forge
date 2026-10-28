import numpy as np
import sub

rng = np.random.default_rng(3)
x = rng.normal(size=(5, 6))
W1, b1 = rng.normal(size=(6, 8)), rng.normal(size=8)
W2, b2 = rng.normal(size=(8, 6)), rng.normal(size=6)


def split(t):
    cols = np.array_split(np.arange(8), t)
    return [W1[:, c] for c in cols], [b1[c] for c in cols], [W2[c, :] for c in cols]


def test_forward_matches_dense():
    dense = np.maximum(x @ W1 + b1, 0) @ W2 + b2
    for t in [1, 2, 4]:
        W1s, b1s, W2s = split(t)
        y, _ = sub.tp_mlp_forward(x, W1s, b1s, W2s, b2)
        assert np.allclose(y, dense)


def test_grad_tp_mlp():
    W1s, b1s, W2s = split(2)
    dy = rng.normal(size=(5, 6))
    y, cache = sub.tp_mlp_forward(x, W1s, b1s, W2s, b2)
    per_rank, db2, dx = sub.tp_mlp_backward(dy, cache, W1s, W2s)

    def loss(x_, W1s_, W2s_):
        return np.sum(sub.tp_mlp_forward(x_, W1s_, b1s, W2s_, b2)[0] * dy)

    for i, j in [(0, 1), (3, 2)]:
        P = [w.copy() for w in W1s]
        P[1][i, j] += 1e-6
        up = loss(x, P, W2s)
        P[1][i, j] -= 2e-6
        assert abs((up - loss(x, P, W2s)) / 2e-6 - per_rank[1][0][i, j]) < 1e-6
        Q = [w.copy() for w in W2s]
        Q[0][j, i] += 1e-6
        up = loss(x, W1s, Q)
        Q[0][j, i] -= 2e-6
        assert abs((up - loss(x, W1s, Q)) / 2e-6 - per_rank[0][2][j, i]) < 1e-6
    for i, j in [(0, 0), (4, 5)]:
        X = x.copy()
        X[i, j] += 1e-6
        up = loss(X, W1s, W2s)
        X[i, j] -= 2e-6
        assert abs((up - loss(X, W1s, W2s)) / 2e-6 - dx[i, j]) < 1e-6
    assert np.allclose(db2, dy.sum(axis=0))
