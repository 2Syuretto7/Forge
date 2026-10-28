import numpy as np
import sub

rng = np.random.default_rng(6)
X = rng.normal(size=(6, 8))
Wq, Wk, Wv = (rng.normal(size=(8, 8)) * 0.5 for _ in range(3))
perm = np.array([3, 0, 5, 1, 4, 2])


def _attn(causal):
    return lambda X: sub.attention(X @ Wq, X @ Wk, X @ Wv, causal=causal)[0]


def test_sinusoidal():
    pe = sub.sinusoidal(5, 4)
    assert pe.shape == (5, 4)
    assert np.allclose(pe[0], [0, 1, 0, 1])
    assert np.isclose(pe[3, 0], np.sin(3)) and np.isclose(pe[3, 3], np.cos(3 / 100))


def test_attention_is_equivariant_without_positions():
    assert sub.is_permutation_equivariant(_attn(False), X, perm)


def test_positions_and_masks_break_equivariance():
    pe = sub.sinusoidal(6, 8)
    with_pos = lambda X: _attn(False)(X + pe)
    assert not sub.is_permutation_equivariant(with_pos, X, perm)
    assert not sub.is_permutation_equivariant(_attn(True), X, perm)
