import numpy as np
import sub

rng = np.random.default_rng(6)


def test_matches_reference():
    Q, K, V = rng.normal(size=(10, 8)), rng.normal(size=(10, 8)), rng.normal(size=(10, 5))
    O, L = sub.flash_attention(Q, K, V, Br=4, Bc=3)
    assert np.allclose(O, sub.reference_attention(Q, K, V))
    S = Q @ K.T / np.sqrt(8)
    assert np.allclose(L, np.log(np.exp(S).sum(axis=1)))


def test_block_sizes_do_not_matter():
    Q, K, V = (rng.normal(size=(12, 4)) * 3 for _ in range(3))
    a, _ = sub.flash_attention(Q, K, V, 1, 1)
    b, _ = sub.flash_attention(Q, K, V, 12, 12)
    c, _ = sub.flash_attention(Q, K, V, 5, 7)
    assert np.allclose(a, b) and np.allclose(b, c)
