import numpy as np
import sub

rng = np.random.default_rng(1)
Q, K, V = (rng.normal(size=(7, 4)) for _ in range(3))


def test_matches_full_attention():
    full = sub.full_attention(Q, K, V)
    cache = {"K": [], "V": []}
    for t in range(7):
        out = sub.cached_attention(Q[t], K[t], V[t], cache)
        assert np.allclose(out, full[t])
    assert len(cache["K"]) == 7
