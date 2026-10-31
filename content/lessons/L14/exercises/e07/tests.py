import numpy as np
import sub

rng = np.random.default_rng(4)
T, d, heads = 6, 16, 8
x = rng.normal(size=(T, d))
Wq, Wk, Wv, Wo = (rng.normal(size=(d, d)) / 4 for _ in range(4))


def test_shards_are_blocks():
    sh = sub.shard_attention(Wq, Wk, Wv, Wo, heads, 4)
    assert len(sh) == 4 and sh[1][0].shape == (16, 4) and sh[1][3].shape == (4, 16)
    assert np.array_equal(sh[1][0], Wq[:, 4:8]) and np.array_equal(sh[3][3], Wo[12:16, :])


def test_tp_attention_matches_dense():
    dense = sub.attention(x, Wq, Wk, Wv, Wo, heads)
    for tp in [1, 2, 4, 8]:
        out = sub.tp_attention(x, sub.shard_attention(Wq, Wk, Wv, Wo, heads, tp), heads // tp)
        assert np.allclose(out, dense)
