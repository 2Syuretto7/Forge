import numpy as np
import sub

rng = np.random.default_rng(2)
Q, K, V = rng.normal(size=(5, 4)), rng.normal(size=(5, 4)), rng.normal(size=(5, 3))


def test_mask():
    m = sub.causal_mask(3)
    assert m.dtype == bool and m.tolist() == [[False, True, True], [False, False, True], [False, False, False]]


def test_against_loops():
    O, P = sub.attention(Q, K, V)
    for i in range(5):
        s = np.array([Q[i] @ K[j] / 2.0 for j in range(i + 1)])
        w = np.exp(s - s.max())
        w /= w.sum()
        assert np.allclose(P[i, : i + 1], w) and np.allclose(P[i, i + 1:], 0)
        assert np.allclose(O[i], w @ V[: i + 1])


def test_options():
    O, P = sub.attention(Q, K, V, causal=False, scale=False)
    S = Q @ K.T
    E = np.exp(S - S.max(axis=1, keepdims=True))
    assert np.allclose(P, E / E.sum(axis=1, keepdims=True))
    assert np.allclose(O, P @ V)
